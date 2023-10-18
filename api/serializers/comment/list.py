from rest_framework import serializers

from api.serializers.user.show import UserShowSerializer
from blog.models import Comment


class CommentlistSerializer(serializers.ModelSerializer):
    author = UserShowSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "title",
            "author",
            "post",
            "created_at",
        )
