from django.http import QueryDict
from rest_framework.response import Response
from rest_framework.views import APIView
from blog.models import Post, Director, Tag
from api.serializers.post.list import PostSerializer
from api.serializers.director.list import DirectorListSerializer
from api.serializers.tag.list import TagListSerializer
from api.service.post.create import PostCreateService
from api.service.post.get import PostDetailService
from api.service.post.delete import PostDeleteService
from api.service.post.filter import PostFilterService
from api.service.post.update import PostUpdateService


class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        """ Отображение постов, в том числе и фильтрация """
        outcome = PostFilterService.execute(request.GET)
        return Response(
            {
                "posts": PostSerializer(outcome.result, many=True).data,
                "tags": TagListSerializer(Tag.objects.all(), many=True).data,
                "directors": DirectorListSerializer(Director.objects.all(), many=True).data
            }
        )


    def post(self, request, *args, **kwargs):
        """ Создание поста """
        data = request.POST.dict() if isinstance(request.POST, QueryDict) else request.POST
        data.update({"user": request.user})
        outcome = PostCreateService.execute(data, request.FILES) # request.POST - словарь, котор хранит в себе данные, передаем внутрь сервиса, request.FILES-фотки
        return Response(PostSerializer(outcome.result).data)


class PostDetailUpdateDestroyView(APIView):
    def get(self, request, *args, **kwargs):
        """ Детальный просмотр поста """
        outcome = PostDetailService.execute(kwargs)
        return Response(
            PostSerializer(outcome.result).data
        )

    def delete(self, request, *args, **kwargs):
        """ Удаление поста """
        kwargs.update({"user": request.user})
        PostDeleteService.execute(kwargs)
        return Response({
            'info': f'Пост с {kwargs["id"]} успешно удален.'
        })

    def patch(self, request, *args, **kwargs):
        """ Редактирование поста """
        data = request.POST.dict() if isinstance(request.POST, QueryDict) else request.POST
        data.update({"user": request.user})
        data.update(kwargs)
        outcome = PostUpdateService.execute(data, request.FILES)
        return Response(
            PostSerializer(outcome.result).data
        )



