from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from .forms import CreateUserForm, UpdateUserForm, CreateIssueForm
from django_email_verification import send_email
from .models import Issue
from .decorators import group_required


def index(request):
    return render(request, "main/index.html")


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username').lower()
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                try:
                    user = User.objects.get(username=username)

                    if user.is_active == False:
                        messages.error(request, 'Twoje konto jest nieaktywne. Potwierdź je za pomocą wiadomości, którą otrzymałeś na adres e-mail podany administratorowi systemu podczas tworzenia konta.')
                        send_email(user)
                except User.DoesNotExist:
                    messages.error(request, 'Login lub hasło są nieprawidłowe.')

        context = {}
        return render(request, 'main/login.html', context)


@group_required('Administrators', raise_exception=True)
def createUser(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if User.objects.filter(username__iexact=request.POST['username']):
            messages.error(request, 'Użytkownik o tym loginie już istnieje.')
            return redirect('create_user')
        elif User.objects.filter(email__iexact=request.POST['email']):
            messages.error(request, 'Użytkownik połączony z tym adresem e-mail już istnieje.')
            return redirect('create_user')
        elif form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            send_email(user)
            user.save()

            if request.POST['role'] == 'user':
                group = Group.objects.get(name='Users')
            elif request.POST['role'] == 'staff':
                group = Group.objects.get(name='Staff')
            group.user_set.add(user)
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Konto użytkownika {username} zostało utworzone. Na podany adres e-mail został wysłany link potwierdzający konto.')
            return redirect('create_user')

    context = {'form': form}
    return render(request, "main/create_user.html", context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.success(request, 'Pomyślnie wylogowano użytkownika.')
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    if request.user.groups.filter(name='Administrators').exists():
        issues = Issue.objects.exclude(status='done').order_by('deadline').all()
    elif request.user.groups.filter(name='Staff').exists():
        issues = Issue.objects.filter(assignee=request.user).exclude(status='done').order_by('deadline').all()
    elif request.user.groups.filter(name='Users').exists():
        issues = Issue.objects.filter(reporter=request.user).exclude(status='done').order_by('deadline').all()
    
    staff = User.objects.filter(groups__name='Administrators') | User.objects.filter(groups__name='Staff')

    context = {'issues': issues, 'staff': staff}
    return render(request, "main/dashboard.html", context)


@login_required(login_url='login')
def settings(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)

        if form.is_valid():
            messages.success(request, 'Dane użytkownika zostały pomyślnie zmodyfikowane.')
            form.save()
            return redirect('settings')
        else:
            messages.error(request, 'Wystąpił błąd poczas modyfikacji danych użytkownika.')
            return redirect('settings')
    else:
        form = UpdateUserForm(instance=request.user)
        context = {'form': form}
        return render(request, 'main/settings.html', context)


@login_required(login_url='login')
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            messages.success(request, 'Hasło zostało zaktualizowane.')
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('settings')
        else:
            messages.error(request, 'Wystąpił błąd podczas aktualizacji hasła. \
            Obecne hasło jest nieprawidłowe, nowe hasło nie spełnia wymagać lub nowe hasło i jego potwierdzenie nie są identyczne.')
            return redirect('change_password')
    else:
        form = PasswordChangeForm(user=request.user)

        context = {'form': form}
        return render(request, 'main/change_password.html', context)


@login_required(login_url='login')
def deleteUser(request, pk):
    user = User.objects.get(id=pk)
    if user is not None:
        user.delete()
        messages.success(request, 'Użytkownik został pomyślnie usunięty.')
        if request.user.id != user.id:
            return redirect('user_management')
        return redirect('login')
    else:
        messages.error(request, 'Wystąpił błąd podczas usuwania użytkownika.')
        return redirect('settings')


@login_required(login_url='login')
def createIssue(request):
    form = CreateIssueForm()

    if request.method == 'POST':
        form = CreateIssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.reporter = request.user
            issue.save()
            messages.success(request, 'Zgłoszenie zostało pomyślnie utworzone.')
            return redirect('dashboard')

    context = {'form': form}
    return render(request, "main/create_issue.html", context)


@login_required(login_url='login')
def updateIssue(request, pk):
    issue = Issue.objects.get(id=pk)

    if request.method == "POST":
        form = CreateIssueForm(request.POST, instance=issue)
        if form.is_valid():
            if request.user.groups.filter(name='Administrators').exists():
                issue.assignee = User.objects.filter(id=request.POST['assignee']).first()
            form.save()
            messages.success(request, 'Zgłoszenie zostało pomyślnie zmodyfikowane.')
            return redirect('dashboard')

    messages.error(request, 'Wystąpił błąd podczas modyfikacji zgłoszenia.')
    return redirect('dashboard')


@login_required(login_url='login')
def deleteIssue(request, pk):
    issue = Issue.objects.get(id=pk)
    
    if request.method == "POST":
        issue.delete()
        messages.success(request, 'Zgłoszenie zostało pomyślnie usunięte.')
        return redirect('dashboard')

    messages.error(request, 'Wystąpił błąd podczas usuwania zgłoszenia.')
    return redirect('dashboard')


@login_required(login_url='login')
def archive(request):
    if request.user.groups.filter(name='Users').exists():
        issues = issues = Issue.objects.filter(reporter=request.user, status='done').order_by('deadline').all()
    else:
        issues = Issue.objects.filter(status='done').order_by('deadline').all()
    
    staff = User.objects.filter(groups__name='Administrators') | User.objects.filter(groups__name='Staff')

    context = {'issues': issues, 'staff': staff}
    return render(request, "main/archive.html", context)


@group_required('Administrators', raise_exception=True)
def statistics(request):
    undone_count = Issue.objects.exclude(status='done').all().count()
    to_do_count = Issue.objects.filter(status='to_do').all().count()
    in_progress_count = Issue.objects.filter(status='in_progress').all().count()
    testing_count = Issue.objects.filter(status='testing').all().count()
    done_count = Issue.objects.filter(status='done').all().count()
    in_processing_count = in_progress_count + testing_count

    sum = amount = 0
    for issue in Issue.objects.filter(status='done').all():
        sum += (issue.updated_at - issue.created_at).days
        amount += 1
    average_processing_time = sum / amount

    amount = 0
    for issue in Issue.objects.filter(status='done').all():
        if issue.updated_at < issue.deadline:
            amount += 1
    accuracy = round((amount / done_count) * 100, 2)
    
    issues_data = {
        'undone_count': undone_count,
        'to_do_count': to_do_count,
        'in_progress_count': in_progress_count,
        'testing_count': testing_count,
        'done_count': done_count,
        'in_processing_count': in_processing_count,
        'average_processing_time': average_processing_time,
        'accuracy': accuracy
    }

    context = {'issues_data': issues_data}
    return render(request, "main/statistics.html", context)


@group_required('Administrators', raise_exception=True)
def userManagement(request):
    users = User.objects.exclude(groups__name='Administrators').all()

    context = {'users': users}
    return render(request, "main/user-management.html", context)


def handler403(request, exception):
    context = {}
    response = render(request, "errors/403.html", context=context)
    response.status_code = 403
    return response


def handler404(request, exception):
    context = {}
    response = render(request, "errors/404.html", context=context)
    response.status_code = 404
    return response


def handler500(request):
    context = {}
    response = render(request, "errors/500.html", context=context)
    response.status_code = 500
    return response