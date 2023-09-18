from rest_framework import serializers
from blog.models import Post
from api.serializers.tag.list import TagListSerializer
from api.serializers.director.list import DirectorListSerializer
from api.serializers.image.list import ImageListSerializer
from api.serializers.user.show import UserShowSerializer


class PostSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(read_only=True, many=True)
    directors = DirectorListSerializer(read_only=True, many=True)
    images = ImageListSerializer(read_only=True, many=True)
    author = UserShowSerializer(read_only=True) # Show or Get показать одного пользователя (many=True НЕТ)


    class Meta:
        model = Post
        # fields = "__all__"
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "updated_at",
            "status",
            "year",
            "author",
            "tags",
            "directors",
            "images",
        )
