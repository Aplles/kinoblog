from functools import lru_cache
from service_objects.services import Service
from django import forms
from blog.models import Post
from rest_framework.exceptions import NotFound

""" Сервис детального получения поста """

class PostDetailService(Service):
    id = forms.IntegerField()

    custom_validations = [
        'post_presence',
    ]

    def run_custom_validations(self):
        for custom_validation in self.custom_validations:
            getattr(self, custom_validation)()

    def process(self):
        self.run_custom_validations()
        self.result = self._post
        return self


    @property
    @lru_cache
    def _post(self) -> [Post, None]:
        try:
            return Post.objects.get(id=self.cleaned_data['id'])
        except Post.DoesNotExist:  # Post.DoesNotExist-нужно указывать модель у которой отлавливаю ошибку
            return None

    def post_presence(self):
        """ Проверка на наличие поста """
        if not self._post:
            raise NotFound(
                {
                    "error": "Поста с таким id не существует."
                }
            )
