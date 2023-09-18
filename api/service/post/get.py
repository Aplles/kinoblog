from service_objects.services import Service
from django import forms
from blog.models import Post
from rest_framework.exceptions import ValidationError


class PostDetailService(Service):
    id = forms.IntegerField()

    custom_validations = [
        'check_post_id',
    ]

    def run_custom_validations(self):
        for custom_validation in self.custom_validations:
            getattr(self, custom_validation)()

    def process(self):
        self.run_custom_validations()
        self.result = self._post
        return self

    @property
    def _post(self) -> Post:
        """
        нужна проверка на существование поста !!!!
        сервис дописать
        """
        return Post.objects.get(id=self.cleaned_data['id'])

    def check_post_id(self):
        "Проверка на наличие поста"
        print("[!] start check_post_id")
        try:
            post = Post.objects.filter(id=self.cleaned_data['id'])
            print("[!] прошел try")
        except DoesNotExist:
            print("[!] НЕ прошел try")
            print(ex)


        # except as ex:
        #     print(ex)
        #     print("[!] НЕ прошел try")


        # except Post.DoesNotExist:
        #     raise ValidationError(
        #         {
        #             "error": "Поста с таким id не существует."
        #         }
        #     )

        # if Post.objects.filter(id=self.cleaned_data['id']):
        #     raise DoesNotExist(
        #         {
        #             "error": "Нет такого поста"
        #         }
        #     )
