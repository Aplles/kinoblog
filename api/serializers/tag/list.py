from rest_framework import serializers
from blog.models import Tag


class TagListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"