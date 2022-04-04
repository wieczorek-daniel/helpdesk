from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
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
            print(username + ' ' + password)
            user = authenticate(request, username=username, password=password)
            print(user)
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


@group_required('Administrators')
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
    issues = Issue.objects.filter(reporter=request.user).order_by('deadline').all()
    context = {'issues': issues}
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