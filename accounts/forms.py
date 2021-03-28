from django import forms
from django.core.exceptions import ValidationError

from .models import RegisterUser


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput, label='Password')
    password_confirm = forms.CharField(max_length=50, widget=forms.PasswordInput, label='Password_Confirm')
    email = forms.EmailField(max_length=50, widget=forms.EmailInput, label='Email')
    first_name = forms.CharField(max_length=50, label='First Name')
    last_name = forms.CharField(max_length=50, label='Last Name')

    def clear_username(self):
        username = self.cleaned_data['username']
        if username:
            check = RegisterUser.objects.filter(username=username).exists()
            if check:
                raise ValidationError(f'Name: {username} already exists')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Password and password_confirm not match')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        user.save()
        return user

    class Meta:
        model = RegisterUser
        fields = ('username', 'password', 'password_confirm', 'email', 'first_name', 'last_name')
