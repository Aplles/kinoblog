from service_objects.services import Service
from django import forms
from blog.models import User
from rest_framework.exceptions import ValidationError

""" Сервис создания пользователя """


class UserCreateService(Service):
    login = forms.CharField()
    password = forms.CharField()
    first_name = forms.CharField(required=False)  # required=False параметр не обязательный
    last_name = forms.CharField(required=False)
    email = forms.CharField(required=False)

    custom_validations = [
        'user_presence',
        'check_len_password',
        'forbidden_symbols',
    ]

    def run_custom_validations(self):
        for custom_validation in self.custom_validations:
            getattr(self, custom_validation)()

    def process(self):
        self.run_custom_validations()
        self.result = self.create()
        return self

    def create(self):
        """ Создали пользователя """
        return User.objects.create_user(
            username=self.cleaned_data['login'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],  # в модели blank=True
            last_name=self.cleaned_data['last_name'],  # в модели blank=True
            email=self.cleaned_data['email']  # в модели blank=True
        )

    def user_presence(self):
        """ Валидация User (проверка, есть ли уже такое имя) """
        if User.objects.filter(username=self.cleaned_data['login']):
            raise ValidationError(
                {
                    "error": "Пользователь с таким login существует. "
                }
            )

    def check_len_password(self):
        """
        Валидация пароля
        -длина от 8 - 12 символов
        """
        if len(self.cleaned_data['password']) < 8 or len(self.cleaned_data['password']) > 12:
            raise ValidationError(
                {
                    "error": "Длина пароля должна быть не меньше 8, не больше 12 знаков."
                }
            )

    def forbidden_symbols(self):
        """ Валидация на запрещенные символы """
        login = self.cleaned_data['login']
        forbidden_symbols = ('?', '#', '<', '>', '%', '@', '/', ' ', '    ', login)
        for symbol in forbidden_symbols:
            if symbol in self.cleaned_data['password']:
                raise ValidationError(
                    {
                        "error": "В пароле нельзя использовать символы '?', '#', '<', '>', '%', '@', '/', ' ', '    '. Пароль не должен совпадать с логином."
                    }
                )
