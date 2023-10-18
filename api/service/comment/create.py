from service_objects.services import Service
from django import forms
from service_objects.fields import ModelField
from blog.models import User, Post, Comment
from rest_framework.exceptions import ValidationError
from api.service.post.get import PostDetailService
from functools import lru_cache

""" Сервис создания комментария """


class CommentCreateService(Service):
    author = ModelField(User)
    title = forms.CharField(required=False)
    id = forms.IntegerField()

    custom_validations = [
        'check_title',
        'check_post',
        'check_len_title',
    ]

    def run_custom_validations(self):
        for custom_validation in self.custom_validations:
            getattr(self, custom_validation)()

    def process(self):
        self.run_custom_validations()
        self.result = self._comment()
        return self

    def _comment(self):
        ''' Создание коммента '''
        return Comment.objects.create(
            title=self.cleaned_data['title'],
            author=self.cleaned_data['author'],
            post=self._post
        )

    @property
    @lru_cache
    def _post(self):
        '''
        Активируется фу-ей check_post.
        Получает экземпляр класса, воспользовавшись сервисом детального
        получения
        '''
        return PostDetailService.execute(self.cleaned_data).result

    def check_title(self):
        ''' Проверка, что title не пустой '''
        if not self.cleaned_data['title']:
            raise ValidationError(
                {
                    "error": "Комментарий не должен быть пустым."
                }
            )

    def check_post(self):
        ''' Проверка существования поста '''
        return self._post

    def check_len_title(self):
        ''' Ограничивает длину комментария '''
        if len(self.cleaned_data['title']) > 255:
            raise ValidationError(
                {
                    "error": "Комментарий не должен больше 255 символов."
                }
            )
