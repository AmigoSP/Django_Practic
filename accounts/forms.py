from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import RegisterUser, PrivateMessage, ChatsFromUsers


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput, label='Password')
    password_confirm = forms.CharField(max_length=50, widget=forms.PasswordInput, label='Password_Confirm')
    email = forms.EmailField(max_length=50, widget=forms.EmailInput, label='Email')
    first_name = forms.CharField(max_length=50, label='First Name')
    last_name = forms.CharField(max_length=50, label='Last Name')

    def clean_username(self):
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


class PrivateMessageAdd(forms.ModelForm):
    from_user = forms.CharField()
    to_user = forms.CharField()
    body = forms.CharField(widget=forms.TextInput)

    def save_chat_user(self):
        try:
            check_main_user = ChatsFromUsers.objects.get(main_user=self.from_user)
        except ChatsFromUsers.DoesNotExist:
            check_main_user = None
        try:
            check_to_user = ChatsFromUsers.objects.get(main_user=self.to_user)
        except ChatsFromUsers.DoesNotExist:
            check_to_user = None
        if not check_main_user:
            new_chat_main_user = ChatsFromUsers.objects.create(main_user=self.from_user)
            new_chat_main_user.save()
            new_chat_main_user.chats_from_users.add(self.to_user)
        else:
            if self.to_user not in check_main_user.chats_from_users.all():
                check_main_user.chats_from_users.add(self.to_user)
        if not check_to_user:
            new_chat_to_user = ChatsFromUsers.objects.create(main_user=self.to_user)
            new_chat_to_user.save()
            new_chat_to_user.chats_from_users.add(self.from_user)
        else:
            if self.from_user not in check_to_user.chats_from_users.all():
                check_to_user.chats_from_users.add(self.from_user)

    def save(self, commit=True):
        self.from_user = User.objects.get(username=self.cleaned_data['from_user'])
        self.to_user = User.objects.get(username=self.cleaned_data['to_user'])
        new_message = super().save(commit=False)
        new_message.body = self.cleaned_data['body']
        new_message.save()
        new_message.from_user.add(self.from_user)
        new_message.to_user.add(self.to_user)
        self.save_chat_user()
        return new_message

    class Meta:
        model = PrivateMessage
        fields = ('body',)
