from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to='image_post/', verbose_name='Изображение')
    current = models.BooleanField(default=False, verbose_name='Главное')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images', verbose_name='Пост')

    def __str__(self):
        return f"{self.post} {self.current}"

    class Meta:
        db_table = 'images_post'
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
