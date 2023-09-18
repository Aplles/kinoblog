from django.http import QueryDict
from rest_framework.response import Response
from rest_framework.views import APIView
from blog.models import Post, Director, Tag
from api.serializers.post.list import PostSerializer
from api.serializers.director.list import DirectorListSerializer
from api.serializers.tag.list import TagListSerializer
from api.service.post.create import PostCreateService
from api.service.post.get import PostDetailService


class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                "posts": PostSerializer(
                    Post.objects.filter(status=Post.PUBLISHED).order_by('-updated_at'), many=True
                ).data,
                "tags": TagListSerializer(Tag.objects.all(), many=True).data,
                "directors": DirectorListSerializer(Director.objects.all(), many=True).data
            }
        )

    # Создание поста
    def post(self, request, *args, **kwargs):
        data = request.POST.dict() if isinstance(request.POST, QueryDict) else request.POST
        data.update({"user": request.user})
        outcome = PostCreateService.execute(data, request.FILES) # request.POST - словарь, котор хранит в себе данные, передаем внутрь сервиса, request.FILES-фотки
        return Response(PostSerializer(outcome.result).data)


class PostDetailUpdateDestroyView(APIView):
    def get(self, request, *args, **kwargs):
        outcome = PostDetailService.execute(kwargs)
        return Response(
            PostSerializer(outcome.result).data
        )