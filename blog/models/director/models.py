# -*- coding: utf8 -*-
from django.db import models


class Director(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    country = models.CharField(max_length=100, verbose_name='Страна')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'director'
        verbose_name = 'Режисер'
        verbose_name_plural = 'Режисеры'
