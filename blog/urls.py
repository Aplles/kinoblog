from django.urls import path

from blog.views.post import PostListView, PostCreateView, PostDetailView, PostDeleteView, PostFilterView
from blog.views.comment import CommentCreateView
from blog.views.user import UserLoginView, UserRegisterView, logout_user


urlpatterns = [    
    path('', PostListView.as_view(), name="index"),
    path('posts/create/', PostCreateView.as_view(), name="create"),

    # path('posts/<int:id>/', PostDetailView.as_view(), name="detail"),
    path('posts/<slug:slug_post>/', PostDetailView.as_view(), name="detail"),
    path('posts/<int:id>/delete_post/', PostDeleteView.as_view(), name="delete_post"),
    path('posts/<slug:slug_post>/comments/', CommentCreateView.as_view(), name="create_comment"),

    path('posts/filters/tags/', PostFilterView.as_view(), name="filter_by_tag"),    
    

    path('user/login/', UserLoginView.as_view(), name="login"),
    path('user/register/', UserRegisterView.as_view(), name="register"),
    path('user/logout/', logout_user, name="logout"),
]
