from rest_framework.views import APIView
from blog.models import Comment
from rest_framework.response import Response
from api.serializers.post.list import PostSerializer
from api.service.comment.get import CommentListServece
from api.service.comment.create import CommentCreateService
from api.serializers.comment.list import CommentlistSerializer
from rest_framework import status
from blog.models import Post
from django.http import QueryDict


class CommentListView(APIView):

    def post(self, request, *args, **kwargs):
        """ Создание комментария"""
        # Если request.POST принадлежит к типу QueryDict - делаем из него словарь
        # в противном случае оставляем без изменений
        data = request.POST.dict() if isinstance(request.POST, QueryDict) else request.POST
        # Обновляю data автором и id-ником
        data.update({"author": request.user}, **kwargs)
        outcome = CommentCreateService.execute(data)
        return Response(CommentlistSerializer(outcome.result).data)