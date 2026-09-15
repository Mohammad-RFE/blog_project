# Admin site registrations and customizations for blog models
from django.contrib import admin
from .models import Article, Category, Tag, Comment

class SlugAdmin(admin.ModelAdmin):
    """
    Admin configuration to automatically populate slug fields from model titles.
    """
    prepopulated_fields = {'slug': ('title',)}

class ArticleAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Article model with enhanced Many-to-Many tag widget.
    """
    filter_horizontal = ('tags',)

# Model registrations
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)