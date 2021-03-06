# Generated by Django 3.1.5 on 2021-03-25 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('body', models.TextField(blank=True, verbose_name='Комментарий')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.registeruser')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('body', models.TextField(verbose_name='Статья')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.registeruser')),
                ('comments', models.ManyToManyField(to='article.Comment')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
    ]
