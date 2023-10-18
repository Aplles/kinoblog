from rest_framework import serializers
from blog.models import Post
from api.serializers.tag.list import TagListSerializer
from api.serializers.director.list import DirectorListSerializer
from api.serializers.image.list import ImageListSerializer
from api.serializers.user.show import UserShowSerializer
from api.serializers.comment.list import CommentlistSerializer


class PostSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(read_only=True, many=True)
    directors = DirectorListSerializer(read_only=True, many=True) # read_only=True-только для чтения, many=True-тк сериализую List(много сериалайзеров)
    images = ImageListSerializer(read_only=True, many=True)
    author = UserShowSerializer(read_only=True) # Show or Get показать одного пользователя (many=True НЕТ)
    comments = CommentlistSerializer(source="comments_post", read_only=True, many=True)


    class Meta:
        model = Post
        # fields = "__all__"
        fields = ( # Если нужно просериализовать конкретное поле (images), то all, не подходит, нужно прописать конкретные поля
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
            "comments"
        )
