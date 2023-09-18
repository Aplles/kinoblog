from functools import lru_cache
from service_objects.services import Service
from django import forms
from blog.models import Post
from rest_framework.exceptions import NotFound


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
        except Post.DoesNotExist:
            return None

    def post_presence(self):
        if not self._post:
            raise NotFound(
                {
                    "error": "Post matching query does not exist."
                }
            )


