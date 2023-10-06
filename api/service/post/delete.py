from functools import lru_cache
from rest_framework.exceptions import PermissionDenied
from service_objects.services import Service
from service_objects.fields import ModelField
from api.service.post.get import PostDetailService
from blog.models import User
from django import forms

""" Сервис удаления поста поста """


class PostDeleteService(Service):
    user = ModelField(User)
    id = forms.IntegerField()

    custom_validations = [
        'check_user',
    ]

    def run_custom_validations(self):
        for custom_validation in self.custom_validations:
            getattr(self, custom_validation)()

    def process(self):
        self.run_custom_validations()
        self._post.delete()
        return self

    @property
    @lru_cache
    def _post(self):
        # Получаю экземпляр класса, воспользовавшись сервисом детального получения
        return PostDetailService.execute(self.cleaned_data).result

    def check_user(self):
        """ Проверка на суперюзера """
        if not self.cleaned_data["user"].is_superuser:
            raise PermissionDenied(
                {
                    "error": "Удалять пост, может superuser."
                }
            )
