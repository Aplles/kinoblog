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
        'check_tags',
        'check_directors',
    ]

    def run_custom_validations(self):
        for custom_validation in self.custom_validations:
            getattr(self, custom_validation)()

    def process(self):
        self.run_custom_validations()
        self.result = self._update()
        return self

    def _update(self):
        post = self._post
        for field in ['title', 'description', 'year', 'status']:
            if self.cleaned_data[field]:
                setattr(post, field, self.cleaned_data[field])

        if self.cleaned_data['title']:
            post.slug = slugify(self.cleaned_data['title'])
        post.save()

        if self.cleaned_data['tags']:
            post.tags.clear()
            post.tags.set(self._tags)
        if self.cleaned_data['directors']:
            post.directors.clear()
            post.directors.set(self._directors)

        return post

    @property
    @lru_cache
    def _tags(self) -> list:
        return [
            Tag.objects.get(id=tag_id)
            for tag_id in self.cleaned_data['tags'].split(',')  # Генератор списка с условием
            if tag_id
        ]

    @property
    @lru_cache
    def _directors(self) -> list:
        return [
            Director.objects.get(id=director_id)
            for director_id in self.cleaned_data['directors'].split(',')
            if director_id
        ]

    @property
    @lru_cache
    def _post(self):
        """
        Проверяю существование поста, воспользовавшись сервисом детального получения
        """
        return PostDetailService.execute(self.cleaned_data).result

    def check_year(self):
        if len(self.cleaned_data['year']) > 4 or not self.cleaned_data['year'].isdigit():
            raise ValidationError(
                {
                    "error": "Значение года должно быть числовым, не 4 символов. "
                }
            )

    def check_status(self):
        if self.cleaned_data['status'] not in ['PB', 'DF', '']:
            raise ValidationError(
                {
                    "error": "Значение status должно быть PB or DF. "
                }
            )

    def check_directors(self) -> None:
        """ Валидация директоров """
        try:
            directors = self._directors
        except Director.DoesNotExist:
            raise ValidationError(
                {
                    "error": "Нет такого режиссера в Базе данных."
                }
            )

    def check_user(self):
        """ Проверка на суперюзера """
        if not self.cleaned_data["user"].is_superuser:
            raise PermissionDenied(
                {
                    "error": "Создавать пост, может superuser."
                }
            )
