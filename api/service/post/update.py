from service_objects.services import Service
from django import forms
from blog.models import User
from service_objects.fields import ModelField
from api.service.post.get import PostDetailService
from functools import lru_cache
from blog.models import User, Tag, Director, Image, Post
from pytils.translit import slugify
from rest_framework.exceptions import ValidationError
from pytils.translit import slugify

""" Сервис редактирования поста """


class PostUpdateService(Service):
    title = forms.CharField(required=False)  # будет в cleaned data, required=False-необязательный аргумент
    description = forms.CharField(required=False)
    year = forms.CharField(
        required=False)  # integerfield не пошло, прилож drf не пропускает, буду конвертировать внутри сервиса
    status = forms.CharField(required=False)
    main_foto = forms.CharField(required=False)
    tags = forms.CharField(required=False)
    directors = forms.CharField(required=False)
    user = ModelField(User)
    id = forms.IntegerField()

    custom_validations = [
        'check_year',
        'check_status',
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
        post.tags.set()
        return post

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