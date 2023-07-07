from django.urls import path

from blog.views.post import PostListView, PostCreateView
from blog.views.user import UserLoginView, UserRegisterView, logout_user

urlpatterns = [
    path('', PostListView.as_view(), name="index"),
    path('posts/create/', PostCreateView.as_view(), name="create"),

    path('user/login/', UserLoginView.as_view(), name="login"),
    path('user/register/', UserRegisterView.as_view(), name="register"),
    path('user/logout/', logout_user, name="logout"),
]
