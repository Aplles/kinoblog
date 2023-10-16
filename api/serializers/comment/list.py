from rest_framework import serializers
from blog.models import Comment
class CommentlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"
        