from django.urls import path
from api.views.post import PostListView, PostDetailUpdateDestroyView

urlpatterns = [
    path('posts/', PostListView.as_view()), # Просмотр,   создание записей
    path('posts/<int:id>/', PostDetailUpdateDestroyView.as_view()), # Детальный просмотр(get), редактирование(path),удаление(delete)
]
