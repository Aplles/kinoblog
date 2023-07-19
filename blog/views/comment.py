from django.shortcuts import redirect, render
from django.views import View

from blog.models import Post, Comment


class CommentCreateView(View):
    '''cоздание комментария'''
    def post(self, request, *args, **kwargs):
        
        title = request.POST['text_comment']
        author = request.user
        post = Post.objects.get(slug=kwargs['slug_post'])

        if title:
            Comment.objects.create(title=title, author=author, post=post)
            return redirect(post.get_absolute_url())
        
        return render(
            request,
            'detail.html',
            context={'post':post, 'error':'В комментрии нет информации'}
        )
        
        
        

        



        