from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound, PermissionDenied
from service_objects.services import Service
from django import forms
from blog.models import User
from functools import lru_cache

""" Сервис авторизации пользователя """

class UserLoginService(Service):
    login = forms.CharField()
    password = forms.CharField()

    custom_validations = [
        'user_presence',
        'check_password',
    ]

    def run_custom_validations(self):
        for custom_validation in self.custom_validations:
            getattr(self, custom_validation)()

    def process(self):
        self.run_custom_validations()
        self.result = self._token.key
        return self

    @property
    @lru_cache
    def _user(self):
        try:
            return User.objects.get(username=self.cleaned_data['login'])
        except User.DoesNotExist:
            return None


    def user_presence(self):
        """ Проверка существования пользователя с таким именем """
        # if not User.objects.filter(username=self.cleaned_data['login']):
        if not self._user:
            raise NotFound(
                {
                    "error": "Такого пользователя не существует."
                }
            )

    def check_password(self):
        """ Проверка правильный ли пароль был введен """
        if not self._user.check_password(self.cleaned_data['password']):
            raise PermissionDenied(
                {
                    "error": "Указан не верный пароль."
                }
            )


    @property
    def _token(self):
        """
        Ф-ия проверки существования токена или выдачи оного, в случае отсутствия
        Ф-ия приватная, потому, что обращаться будем только в этом классе
        """
        try:
            return Token.objects.get(user=self._user)
        except Token.DoesNotExist:
            return Token.objects.create(user=self._user)
