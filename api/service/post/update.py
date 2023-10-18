from service_objects.services import Service
from django import forms
from blog.models import User
from service_objects.fields import ModelField
from api.service.post.get import PostDetailService
from functools import lru_cache
from blog.models import User, Tag, Director, Image, Post
from pytils.translit import slugify
from rest_framework.exceptions import ValidationError, PermissionDenied
from pytils.translit import slugify

""" Сервис редактирования поста """


class PostUpdateService(Service):
    title = forms.CharField(required=False)
    description = forms.CharField(required=False)
    year = forms.CharField(required=False)
    status = forms.CharField(required=False)
    main_foto = forms.CharField(required=False)
    tags = forms.CharField(required=False)
    directors = forms.CharField(required=False)
    user = ModelField(User)
    id = forms.IntegerField()

    custom_validations = [
        'check_year',
        'check_status',
        'check_directors',
        'check_tags',
        'check_user',
        'check_count_photo',
        'check_main_photo'
    ]

    def run_custom_validations(self):
        for custom_validation in self.custom_validations:
            getattr(self, custom_validation)()

    def process(self):
        self.run_custom_validations()
        self.result = self._update()
        self.update_photo()
        return self

    def _update(self):
        post = self._post
        ''' Проверка, какие поля изменил пользователь (без тегов и режиссеров) '''
        for field in ['title', 'description', 'year', 'status']:
            if self.cleaned_data[field]:
                # setattr обращаюсь к объекту, полю, его значению
                setattr(post, field, self.cleaned_data[field])

        ''' Создание slug  '''
        if self.cleaned_data['title']:
            post.slug = slugify(self.cleaned_data['title'])
        post.save()

        """ Если есть новые теги, очищаем старые, устанавлинваем новые """
        if self.cleaned_data['tags']:
            post.tags.clear()
            post.tags.set(self._tags)
        """ Если есть новые режиссеры, очищаем старые, устанавлинваем новые """
        if self.cleaned_data['directors']:
            post.directors.clear()
            post.directors.set(self._directors)

        return post

    def check_year(self):
        """ Валидация года """
        if len(self.cleaned_data['year']) > 4 or not self.cleaned_data['year'].isdigit():  # .isdigit()-является числом
            raise ValidationError(
                {
                    "error": "Значение года должно быть числовым, не 4 символов. "
                }
            )

    def check_status(self):
        """ Валидация статуса """
        if self.cleaned_data['status'] not in ['PB', 'DF', '']:
            raise ValidationError(
                {
                    "error": "Значение status должно быть PB or DF. "
                }
            )

    def check_directors(self) -> None:
        """
        Вывод ошибки, если id директора, нет в БД
        Обращается к _directors (поиск по id в БД), выводит ошибку
        если такого директора нет
        """
        try:
            directors = self._directors
        except Director.DoesNotExist:
            raise ValidationError(
                {
                    "error": "Нет такого режиссера в Базе данных."
                }
            )

    @property
    @lru_cache
    def _directors(self) -> list:
        """
        Поиск директора по id в БД, отправка ответа в  check_directors
        """
        return [
            Director.objects.get(id=director_id)
            for director_id in self.cleaned_data['directors'].split(',')
            if director_id
        ]

    def check_tags(self) -> None:
        """
        Вывод ошибку, если id тега, нет в БД
        Обращается к _tags (поиск по id в БД), выводит ошибку
        если такого тега нет
        """
        try:
            tags = self._tags
        except Tag.DoesNotExist:
            raise ValidationError(
                {
                    "error": "Нет такого тега в Базе данных."
                }
            )

    @property
    @lru_cache
    def _tags(self) -> list:
        """
        Поиск тега по id в БД, отправка ответа в check_tags
        """
        return [
            Tag.objects.get(id=tag_id)
            for tag_id in self.cleaned_data['tags'].split(',')  # Генератор списка с условием
            if tag_id
        ]

    @property
    @lru_cache
    def _post(self):
        """
        Проверяю существование поста, воспользовавшись сервисом детального получения
        """
        return PostDetailService.execute(self.cleaned_data).result

    def check_user(self):
        """ Проверка на суперюзера """
        if not self.cleaned_data["user"].is_superuser:
            raise PermissionDenied(
                {
                    "error": "Создавать, редактировать пост, может superuser."
                }
            )

    def update_photo(self):
        ''' Обновление фотографий. Все предыдущие удаляются! '''
        if not self.files:
            return
        Image.objects.filter(post=self._post).delete()
        for name, photo in self.files.items():
            Image.objects.create(
                image=photo,
                post=self._post,
                current=name.split('_')[-1] == self.cleaned_data['main_foto']
            )

    def check_count_photo(self):
        if len(self.files) > 4:
            raise ValidationError(
                {
                    "error": "Максимум 4 фотографии."
                }
            )

    def check_main_photo(self):
        if self.cleaned_data['main_foto'] not in [key.split("_")[-1] for key in self.files.keys()]:
            raise ValidationError(
                {
                    "error": "Главная фотография не выбрана, или выбрана не правильно"
                }
            )
