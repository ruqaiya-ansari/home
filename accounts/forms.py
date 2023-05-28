from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
from django.contrib.auth import authenticate, login


class MyAuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(MyAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username', 'id': 'login_username'})
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'login_password'})
        self.fields['password'].label = False


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username'})
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password'].label = False
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
        self.fields['password2'].label = False
        self.fields['email'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'})
        self.fields['email'].label = False
        self.fields['first_name'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['first_name'].label = False

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords does not match')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['first_name'].label = False
        self.fields['last_name'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['last_name'].label = False
        self.fields['email'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'})
        self.fields['email'].label = False


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)

        self.fields['photo'].label = False
        self.fields['date_of_birth'].label = False
