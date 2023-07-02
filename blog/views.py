from django.shortcuts import render
from django.views import View

from blog.models import Post


class MainPage(View):

    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(status=Post.PUBLISHED).order_by(
            '-updated_at')
        return render(request, 'index.html', context={
            'posts': posts
        })

    def post(self, request, *args, **kwargs):
        data = request.POST  # Словарь с данными из формы
        # Создать пост и картинки к посту.
        pass
