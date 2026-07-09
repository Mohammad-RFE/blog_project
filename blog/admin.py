from django.contrib import admin
from .models import Article, Category, Tag, Comment

class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)

