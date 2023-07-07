# -*- coding: utf8 -*-
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model

from blog.models import Post

User = get_user_model()


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', max_length=255,
                               widget=forms.TextInput(attrs={'id': 'textArea', 'class': 'login'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(
                                    attrs={'id': 'textArea', 'class': 'password'}))
    password2 = forms.CharField(label='Повтор пароля',
                                widget=forms.PasswordInput(
                                    attrs={'id': 'textArea', 'class': 'password'}))

    class Meta:
        model = User
        fields = ("username", 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', max_length=255,
                               widget=forms.TextInput(attrs={'id': 'textArea', 'class': 'login'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(
                                   attrs={'id': 'textArea', 'class': 'password'}))


class PostAddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'description',
            'status',
            'tags',
            'directors',
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-post-class'}),
            'description': forms.Textarea(attrs={'class': 'input-post-class'}),
        }

# class OrderAddForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = (
#             'payment_method',
#         )
