from django.db import models

class Comment(models.Model):
    title = models.TextField(verbose_name='Заголовок')    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comments_user', verbose_name='Автор')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments_post', verbose_name='Пост')

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
