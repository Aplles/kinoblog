# -*- coding: utf8 -*-
from django.db import models


class Post(models.Model):
    DRAFT = 'DF'
    PUBLISHED = 'PB'

    STATUS = [
        (DRAFT, 'Черновик'),
        (PUBLISHED, 'Опубликовано'),
    ]

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='Слаг')
    description = models.TextField(verbose_name='Описание')
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=DRAFT
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='posts_author'
    )
    tags = models.ManyToManyField('Tag', verbose_name='Теги')
    directors = models.ManyToManyField('Director', verbose_name='Режисcеры')

    def image(self):
        return self.images.get(current=True).image.url

    def __str__(self):
        return f'{self.title} {self.author}'

    class Meta:
        db_table = 'posts'
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
