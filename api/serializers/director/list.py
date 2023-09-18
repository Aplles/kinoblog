from rest_framework import serializers
from blog.models import Director


class DirectorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Director
        fields = "__all__"