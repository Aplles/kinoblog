from service_objects.services import Service
from service_objects.fields import ModelField
from blog.models import User, Post
from django import forms


class PostDeleteService(Service):
    user = ModelField(User)
    id = forms.IntegerField()

    def process(self):
        return self



