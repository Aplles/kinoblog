from django.shortcuts import redirect
from django.views import View

from blog.models import Post, Comment


class CommentCreateView(View):
    '''cоздание комментария'''
    def post(self, request, *args, **kwargs):
        
        title = request.POST['text_comment']
        author = request.user
        post = Post.objects.get(slug=kwargs['slug_post'])
        Comment.objects.create(title=title, author=author, post=post)
        print(post.get_absolute_url())

        return redirect(post.get_absolute_url())



        