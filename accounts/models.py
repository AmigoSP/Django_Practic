from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class RegisterUser(User):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class PrivateMessage(models.Model):
    from_user = models.ManyToManyField(User, related_name='from_user')
    to_user = models.ManyToManyField(User, related_name='to_user')
    body = models.TextField(verbose_name='message')
    date = models.DateTimeField(auto_created=True, auto_now_add=True)
    reading = models.BooleanField(default=False, verbose_name='it_reading')

    class Meta:
        verbose_name = 'Личное сообщение'
        verbose_name_plural = "Личные сообщения"


class ChatsFromUsers(models.Model):
    main_user = models.ForeignKey(User, on_delete=models.PROTECT)
    chats_from_users = models.ManyToManyField(User, related_name='chats_from_users')

