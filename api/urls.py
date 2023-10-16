from django.urls import path
from api.views.post import PostListView, PostDetailUpdateDestroyView
from api.views.user import UserLoginView, UserCreateView
from api.views.comment import CommentListView

urlpatterns = [
    path('posts/', PostListView.as_view()), # Просмотр постов, просмотр отфильтрованных, создание постов
    path('posts/<int:id>/', PostDetailUpdateDestroyView.as_view()), # Детальный просмотр(get), редактирование(path),удаление(delete)
    path('users/auth/', UserLoginView.as_view()),
    path('users/register/', UserCreateView.as_view()),
    # path('posts/comments/', CommentCreate.as_view()), # Создание комментов
    path('posts/<int:id>/comments/', CommentListView.as_view()), # Просмотр(get), Создание комментариев(post)
]


