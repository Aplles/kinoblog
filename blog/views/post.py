from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.views import View

from blog.forms import PostAddForm
from blog.models import Post, Tag, Director


class PostListView(View):

    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(status=Post.PUBLISHED).order_by(
            '-updated_at')
        return render(request, 'index.html', context={
            'posts': posts
        })


class PostCreateView(View):

    def get(self, request):
        return render(request, 'create.html', context={
            'form': PostAddForm()
        })

    def post(self, request, *args, **kwargs):
        post = Post.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            status=request.POST['status'],
            author=request.user,
            slug=slugify(request.POST['title'])
        )
        tags = [Tag.objects.get(id=tag_id) for tag_id in request.POST.getlist('tags')]
        # tags = []
        # for tag_id in request.POST.getlist('tags'):
        #     tags.append(Tag.objects.get(id=tag_id))
        directors = [
            Director.objects.get(id=director_id)
            for director_id in request.POST.getlist('directors')
        ]
        post.tags.set(tags)
        post.directors.set(directors)
        return redirect("index")
    

class PostDetailView(View):
    ''' Детальное отображение поста '''

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs['id'])
        return render(
            request,
            'detail.html',
            context={'post':post}
        )
    

class PostDeleteView(View):
    ''' удаление поста '''

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs['id'])        
        post.delete()
        return redirect("index")
