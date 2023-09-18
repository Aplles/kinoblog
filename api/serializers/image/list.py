from rest_framework import serializers
from blog.models import Image


class ImageListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        # fields = "__all__"
        exclude = ("post", )
