from service_objects.services import Service
from django import forms
from blog.models import User, Tag, Director, Image, Post
from pytils.translit import slugify
from service_objects.fields import ModelField
from functools import lru_cache
from rest_framework.exceptions import ValidationError, PermissionDenied


""" Сервис создания поста поста """


class PostCreateService(Service):
    title = forms.CharField(required=False)  # будет в cleaned data, required=False-необязательный аргумент
    description = forms.CharField()
    year = forms.CharField()  # integerfield не пошло, прилож drf не пропускает, буду конвертировать внутри сервиса
    status = forms.CharField()
    main_foto = forms.CharField()
    tags = forms.CharField()
    directors = forms.CharField()
    user = ModelField(User)

    # Список хранит название функций, которые я буду запускать в цикле
    custom_validations = [
        'check_status',
        'check_tags',
        'check_slug',
        'check_photo',
        'check_year',
        'check_directors',
        'check_user',
    ]
    def run_custom_validations(self):
        for custom_validation in self.custom_validations:
            getattr(self, custom_validation)()

    def process(self):
        self.run_custom_validations()
        '''
        Основная функция, всегда такое имя, запуск кода всегда начинается с нее
        В других фу-ях пишу логику, а в def process вызываю эти функции

        Если внутри сервиса создать каки-то локальные сво-ва,
        и возвращать self из метода process, то я могу оперировать
        этими локальными сво-ми через метод outcome
        '''

        self._images(self._post)
        self.result = self._post
        return self

    @property
    @lru_cache
    def _post(self) -> Post:
        post = Post.objects.create(
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            year=self.cleaned_data['year'],
            status=self.cleaned_data['status'],
            author=self.cleaned_data['user'],
            slug=slugify(self.cleaned_data['title'])
        )
        post.tags.set(self._tags)
        post.directors.set(self._directors)
        return post

    def _images(self, post: Post) -> None:
        ''' Создание картинок '''
        index_main_foto = self.cleaned_data['main_foto']
        for name, foto in self.files.items():
            Image.objects.create(
                image=foto,
                current=index_main_foto == name[-1],
                post=post
            )

    @property
    @lru_cache
    def _tags(self) -> list:
        ''' Создание тегов '''
        return [
            Tag.objects.get(id=tag_id)
            for tag_id in self.cleaned_data['tags'].split(',')  # Генератор списка с условием
            if tag_id
        ]

    @property
    @lru_cache
    def _directors(self) -> list:
        ''' Создание директоров '''
        return [
            Director.objects.get(id=director_id)
            for director_id in self.cleaned_data['directors'].split(',')
            if director_id
        ]

    def check_status(self) -> None:
        """ Валидация статуса """
        if self.cleaned_data['status'] not in [Post.DRAFT, Post.PUBLISHED]:
            raise ValidationError(
                {
                    "error": f"Status must be a {Post.DRAFT} or {Post.PUBLISHED}."
                }
            )

    def check_tags(self) -> None:
        """ Валидация тегов """
        try:
            tags = self._tags
        except Tag.DoesNotExist:
            raise ValidationError(
                {
                    "error": "Tag matching query does not exist."
                }
            )

    def check_slug(self) -> None:
        """ Валидация слага """
        if Post.objects.filter(slug=slugify(self.cleaned_data['title'])):
            raise ValidationError(
                {
                    "error": "Пост с этим slug уже существует. "
                }
            )

    def check_photo(self) -> None:
        """ Валидация фотографий """
        main_photo = self.cleaned_data['main_foto']
        list_index = [key.split("_")[-1] for key in self.files.keys()]
        if main_photo not in list_index:
            raise ValidationError(
                {
                    "error": "Фотография может иметь только числовой индекс"
                }
            )
        if len(self.files) > 4:
            raise ValidationError(
                {
                    "error": "Максимальное количество фото 4 шт. ."
                }
            )

    def check_year(self) -> None:
        """ Валидация года """
        try:
            year = int(self.cleaned_data['year'])
        except ValueError:
            raise ValidationError(
                {
                    "error": "Год должен быть числом."
                }
            )
        if year < 0:
            raise ValidationError(
                {
                    "error": "Год должен быть положительным числом."
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
        """ Проверка на суперюзера"""
        if not self.cleaned_data["user"].is_superuser:
            raise PermissionDenied(
                {
                    "error": "Создавать пост, может superuser."
                }
            )


