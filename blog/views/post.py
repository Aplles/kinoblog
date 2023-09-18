from django.db.models import Exists, Count, Q
from django.shortcuts import render, redirect
from pytils.translit import slugify
from django.views import View

from blog.forms import PostAddForm
from blog.models import Post, Tag, Director, Image
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
        # print("directors:", directors)\

        # пагинация
        # экземпляр класса Paginator с числом объектов, возвращаемых на страницу
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page', 1)
        try:
            posts = paginator.page(page_number)

        # если вызванная страница не int, выдать первую
        except PageNotAnInteger:
            posts = paginator.page(1)

        # если вызванная страница вне диапазона, выдать последнюю
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

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


class PostRedactionView(LoginRequiredMixin, View):
    ''' Редактирование поста '''

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs['id'])
        tags = Tag.objects.annotate(is_tagged=Count('posts_tag', filter=Q(posts_tag__id=post.id))).all()
        directors = Director.objects.annotate(
            is_director=Count('posts_director', filter=Q(posts_director__id=post.id))).all()
        return render(
            request,
            'redaction.html',
            context={
                'post': post,
                'tags': tags,
                'directors': directors,
                "count_new_photo": ''.join([str(i) for i in range(post.images.all().count() + 1, 5)])
            }
        )

    """ Редактирование поста """

    def post(self, request, *args, **kwargs):
        # по id достаю из БД нужный пост
        global post
        post = Post.objects.get(id=kwargs['id'])

        # из запроса получаю title
        title = request.POST.get('title')

        # если title не пустой
        if title:
            # перезаписываю новый title
            post.title = title

            # записываю новый slug
            post.slug = slugify(title)

        # из запроса достаю description
        description = request.POST.get('description')

        # если  description есть
        if description:
            # в модели поста перезаписываю description
            post.description = description

        # из запроса получаю год
        year = request.POST.get('year')

        # если год есть, перезаписываю его в модели поста, изменив тип данных на число
        # а если нет или строка, то год не запишется
        if year:
            try:
                post.year = int(year)
            except ValueError:
                ...

        # получаю из запроса статус
        status = request.POST.get('status')

        # меняю (если поменялся) в модели поста статус
        # а если черновик, тогда Что??????
        if status:
            if status == Post.PUBLISHED:
                post.status = Post.PUBLISHED
            else:
                post.status = Post.DRAFT

        directors = []
        tags = []
        # выдергиваю все id тегов у поста, записываю их в список
        # когда я провалюсь в except??????
        for key, value in request.POST.items():
            if 'tag_' in key:
                try:
                    tag = Tag.objects.get(id=value)
                    tags.append(tag)
                except Tag.DoesNotExist:
                    ...
            # Выдергиваю все id режиссеров, записываю их в список
            elif 'dir_' in key:
                try:
                    director = Director.objects.get(id=value)
                    directors.append(director)
                except Director.DoesNotExist:
                    ...
        # если список с тегами не пустой, очищаю в БД теги, предыдущие теги, устанавливаю новые
        if tags:
            post.tags.clear()
            post.tags.set(tags)
        if directors:
            post.directors.clear()
            post.directors.set(directors)
        post.save()

        current_image_id = int(request.POST['main_foto'])  # 3 или -2, id или index

        if current_image_id < 0:  # если пришел index (они отрицательные)
            for photo in post.images.all():
                photo.current = False # удаляю предыдущую отметку "Основное фото"
                photo.save()
            for key, value in request.FILES.items():
                # key = foto_-2  [foto, '-2']
                # если индекс и foto_index совпали, то фото запишем основным
                if current_image_id == int(key.split("_")[-1]):
                    Image.objects.create(
                        image=value,
                        current=True, # основное
                        post=post
                    )
                # если индекс и foto_index НЕ совпали, то фото не основное
                else:
                    Image.objects.create(
                        image=value,
                        current=False, # не основное
                        post=post
                    )
        else:  # Пришел id (фото уже были записаны раньше в БД)
            for photo in post.images.all():
                if current_image_id == photo.id:
                    photo.current = True
                else:
                    photo.current = False
                photo.save()
            for key, value in request.FILES.items():
                # если при итерации пар попадется индекс (он отрицательный!)
                try:
                    image = Image.objects.get(id=key.split("_")[-1])
                    image.image = value
                    image.save()
                except Image.DoesNotExist:
                    Image.objects.create(
                        image=value,
                        current=False,
                        post=post
                    )
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
