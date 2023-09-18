from rest_framework import serializers
from blog.models import User


class UserShowSerializer(serializers.ModelSerializer): # Show or Get показать одного пользователя

    class Meta:
        model = User
        # fields = "__all__"
        exclude = (
            "password",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions"
        )