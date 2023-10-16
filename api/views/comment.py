from rest_framework.views import APIView
from blog.models import Comment
from rest_framework.response import Response
from api.serializers.post.list import PostSerializer
from api.service.comment.get import CommentListServece
from api.service.comment.create import CommentCreateServece
from api.serializers.comment.list import CommentlistSerializer
from rest_framework import status
from blog.models import Post
from django.http import QueryDict


class CommentListView(APIView):
    """ Просмотр комментариев"""
    def get(self, request, *args, **kwargs):
        comments = Comment.objects.all()
        # outcome = CommentListServece.execute()
        return Response({
            "comments": CommentlistSerializer(
                Comment.objects.all().order_by('-created_at'), many=True
            ).data,
            "posts": PostSerializer(
                Post.objects.filter(status=Post.PUBLISHED).order_by('-updated_at'), many=True
            ).data,
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """ Создание комментария"""
        # Если request.POST принадлежит к типу QueryDict - делаем из него словарь
        # в противном случае оставляем без изменений
        data = request.POST.dict() if isinstance(request.POST, QueryDict) else request.POST
        data.update({"author": request.user}, **kwargs)
        outcome = CommentCreateServece.execute(data)
        return Response(CommentlistSerializer(outcome.result).data)