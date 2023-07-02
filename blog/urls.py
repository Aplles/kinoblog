from django.urls import path

from blog.views import MainPage

urlpatterns = [
    path('', MainPage.as_view(), name="index"),
]
