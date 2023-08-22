from django.db.models import Exists, Count, Q
from django.shortcuts import render, redirect
from pytils.translit import slugify
from django.views import View

from blog.forms import PostAddForm
from blog.models import Post, Tag, Director, Image
from django.contrib.auth.models import AnonymousUser

'''
тестовая запись для github
'''


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

        index_main_foto = request.POST['main_foto']
        for name, foto in request.FILES.items():
            Image.objects.create(
                image=foto,
                current=index_main_foto == name[-1],
                post=post
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
        tags = Tag.objects.annotate(is_tagged=Count('posts_tag', filter=Q(posts_tag__id=post.id))).all()
        directors = Director.objects.annotate(
            is_director=Count('posts_director', filter=Q(posts_director__id=post.id))).all()
        count_new_photo = 4 - post.images.all().count()
        return render(
            request,
            'redaction.html',
            context={
                'post': post,
                'tags': tags,
                'directors': directors,
                "count_new_photo": count_new_photo
            }
        )

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs['id'])
        title = request.POST.get('title')
        if title:
            post.title = title
            post.slug = slugify(title)
        description = request.POST.get('description')
        if description:
            post.description = description
        year = request.POST.get('year')
        if year:
            try:
                post.year = int(year)
            except ValueError:
                ...
        status = request.POST.get('status')
        if status:
            if status == Post.PUBLISHED:
                post.status = Post.PUBLISHED
            else:
                post.status = Post.DRAFT

        directors = []
        tags = []
        for key, value in request.POST.items():
            if 'tag_' in key:
                try:
                    tag = Tag.objects.get(id=value)
                    tags.append(tag)
                except Tag.DoesNotExist:
                    ...
            elif 'dir_' in key:
                try:
                    director = Director.objects.get(id=value)
                    directors.append(director)
                except Director.DoesNotExist:
                    ...
        if tags:
            post.tags.clear()
            post.tags.set(tags)
        if directors:
            post.directors.clear()
            post.directors.set(directors)
        post.save()

        current_image_id = request.POST['main_foto']
        for photo in post.images.all():
            if int(current_image_id) == photo.id:
                photo.current = True
            else:
                photo.current = False
            photo.save()

        for key, value in request.FILES.items():
            image = Image.objects.get(id=key.split("_")[-1])
            image.image = value
            image.save()
        return redirect(post.get_absolute_url())


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
