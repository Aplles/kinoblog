# Generated by Django 4.1.4 on 2023-07-02 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('country', models.CharField(max_length=100, verbose_name='Страна')),
            ],
            options={
                'verbose_name': 'Режисер',
                'verbose_name_plural': 'Режисеры',
                'db_table': 'director',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=250, unique=True, verbose_name='Слаг')),
                ('description', models.TextField(verbose_name='Описание')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('status', models.CharField(choices=[('DF', 'Черновик'), ('PB', 'Опубликовано')], default='DF', max_length=2)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts_author', to=settings.AUTH_USER_MODEL)),
                ('director', models.ManyToManyField(to='blog.director', verbose_name='Режисеры')),
                ('tags', models.ManyToManyField(to='blog.tag', verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
                'db_table': 'post',
            },
        ),
    ]
