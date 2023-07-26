from django.db.models import Exists, Count, Q
from django.shortcuts import render, redirect
from pytils.translit import slugify
from django.views import View

from blog.forms import PostAddForm
from blog.models import Post, Tag, Director
from django.contrib.auth.models import AnonymousUser


class PostListView(View):

    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(status=Post.PUBLISHED).order_by(
            '-updated_at')

        tags = Tag.objects.all()
        directors = Director.objects.all()

        # print("tags:", tags, "\n")
        # print("directors:", directors)

        return render(request, 'index.html', context={
            'posts': posts,
            'tags': tags,
            'directors': directors,
        })


class PostCreateView(View):

    def get(self, request):
        if not request.user.is_staff:
            return redirect("index")

        return render(request, 'create.html', context={
            'form': PostAddForm()
        })

    def post(self, request, *args, **kwargs):
        post = Post.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            year=request.POST['year'],
            status=request.POST['status'],
            author=request.user,
            slug=slugify(request.POST['title'])
        )
        print(request.POST['title'])
        print(slugify(request.POST['title']))

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
        if not Post.objects.filter(slug=kwargs['slug_post']):
            return redirect("index")

        post = Post.objects.get(slug=kwargs['slug_post'])
        return render(
            request,
            'detail.html',
            context={'post': post}
        )


class PostDeleteView(View):
    ''' удаление поста '''

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs['id'])
        post.delete()
        return redirect("index")


class PostRedactionView(View):
    ''' Редактирование поста '''

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs['id'])

        tags = Tag.objects.annotate(is_tagged=Count('posts', filter=Q(posts__id=post.id))).all()
        print('[!!!]', tags[0].is_tagged)
        directors = Director.objects.all()

        # print('self:', self)
        # print('request:', request)
        # print('args:', args)
        # print('kwargs:', kwargs)

        return render(
            request,
            'redaction.html',
            context={
                'post': post,
                'tags': tags,
                'directors': directors
            }
        )

    # def post(self, request, *args, **kwargs):
    #     print('self:', self)
    #     print('request:', request)
    #     print('args:', args)
    #     print('kwargs:', kwargs)

    # #     post = Post.objects.filter(id=kwargs['id'])
    #     post = Post.objects.filter(id=kwargs['id'])
    #     return render(
    #     request,
    #     'redaction.html',
    #     context={'posts':post}
    #     )

    # if request.method == 'POST':
    #     print('Я здесь')

    # def get(self, request, *args, **kwargs):
    #         print('self:', self)
    #         print('request:', request)
    #         

    # if request.method == 'GET':

    #


class PostFilterView(View):
    '''вывод постов по тегу'''

    def get(self, request, *args, **kwargs):

        dir_id = []
        tags_id = []
        for key, value in request.GET.items():
            # if key.startswith("tag_"): 
            if 'tag_' in key:
                tags_id.append(value)

            elif 'dir_' in key:
                dir_id.append(value)
        posts = Post.objects.all()
        if tags_id:
            posts = posts.filter(tags__id__in=tags_id)

        if dir_id:
            posts = posts.filter(directors__id__in=dir_id)

        return render(request, 'index.html', context={
            'posts': posts,
            'tags': Tag.objects.all(),
            'directors': Director.objects.all(),
        })
