from django.contrib import admin
from .models import Post, Tag, Director, Image, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'updated_at']
    list_filter = ['status', 'author', 'updated_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'updated_at'
    ordering = ['status', 'updated_at']
    filter_horizontal = (
        "directors",
        "tags"
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
