from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class RegisterUser(User):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
