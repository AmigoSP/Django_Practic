from django.db import models

# Create your models here.
from accounts.models import RegisterUser


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Статья')
    author = models.ForeignKey(RegisterUser, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_created=True, auto_now=True)
    comments = models.ManyToManyField('Comment')
    changed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    body = models.TextField(verbose_name='Комментарий', blank=True)
    author = models.ForeignKey(RegisterUser, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_created=True, auto_now=True)
    changed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
