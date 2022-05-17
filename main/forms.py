from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Issue

class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Hasło'
        self.fields['password2'].label = 'Potwierdzenie hasła'

    class Meta:
        model = User
        
        for value in ('first_name', 'last_name', 'email'):
            model._meta.get_field(value).blank = False
            model._meta.get_field(value).null = False
        model._meta.get_field('email')._unique = True

        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels  = {
            'username':'Login', 
            'first_name':'Imię',
            'last_name':'Nazwisko',
            'email':'Adres e-mail',
            'password1':'Hasło',
            'password2':'Potwierdzenie hasła',
        }


class UpdateUserForm(ModelForm):
    class Meta:
        model = User

        fields = ['email', 'first_name', 'last_name']
        labels  = {
            'email':'Adres e-mail',
            'first_name':'Imię',
            'last_name':'Nazwisko',
        }


class CreateIssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'deadline', 'status']
