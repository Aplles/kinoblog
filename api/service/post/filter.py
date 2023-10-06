from service_objects.services import Service
from blog.models import Post
from functools import lru_cache


class PostFilterService(Service):
    """
    Не создаю cleaned_data, потому что этих пара-ов может не быть
    (если фильтры не задействованы)
    """

    def process(self):
        self.result = self._posts
        return self

    @property
    @lru_cache
    def _directors(self):
        """ Собираю в список всех директоров
        Генератор списка с условием, значения автоматически аппендятся в value """
        return [value for key, value in self.data.items() if 'dir_' in key]

    @property
    @lru_cache
    def _tags(self):
        """ Собираю в список все теги """
        return [value for key, value in self.data.items() if 'tag_' in key]

    @property
    def _posts(self):
        """ Фильтрую посты по тегам и директорам """
        posts = Post.objects.filter(status=Post.PUBLISHED)
        if self._tags:
            '''
            tags__id__in
            захожу в таблицу с тегами, смотрю на их id, 
            это значение должно быть в self._tags'''
            posts = posts.filter(tags__id__in=self._tags)
        if self._directors:
            posts = posts.filter(directors__id__in=self._directors)
        return posts.order_by('-updated_at')    # order_by-именно здесь, это оптимизация!
