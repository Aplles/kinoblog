from service_objects.services import Service
from django import forms
from service_objects.fields import ModelField
from blog.models import User, Post, Comment
from rest_framework.exceptions import ValidationError
from api.service.post.get import PostDetailService
from functools import lru_cache


""" Сервис создания комментария """
class CommentCreateServece(Service):
    author = ModelField(User)
    title = forms.CharField(required=False)
    id = forms.IntegerField()

    custom_validations = [
        'check_title',
        '_post',
        # 'check_len_title',
    ]

    def run_custom_validations(self):
        for custom_validation in self.custom_validations:
            getattr(self, custom_validation)()


    def process(self):
        self.run_custom_validations()
        self.result = self._comment()
        return self

    def _comment(self):
        title = self.cleaned_data['title']
        author = self.cleaned_data['author']
        post = Post.objects.get(id=self.cleaned_data['id'])

        if title:
            return Comment.objects.create(title=title, author=author, post=post)

    def check_title(self):
        if not self.cleaned_data['title']:
            raise ValidationError(
                {
                    "error": "Комментарий не должен быть пустым."
                }
            )

    @property
    @lru_cache
    def _post(self):
        # Получаю экземпляр класса, воспользовавшись сервисом детального получения
        return PostDetailService.execute(self.cleaned_data).result


    def check_len_title(self):
        if len(self.cleaned_data['title']) > 255:
            ...
