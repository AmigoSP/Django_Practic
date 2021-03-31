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
    date = models.DateField(auto_created=True, auto_now=True)
    reading = models.BooleanField(default=False, verbose_name='it_reading')

    class Meta:
        verbose_name = 'Личное сообщение'
        verbose_name_plural = "Личные сообщения"
