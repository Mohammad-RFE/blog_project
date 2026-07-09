from .models import Category, Tag, Article

def sidebar(request):
    return {
        "global_categories": Category.objects.all(),
        "global_tags": Tag.objects.all(),
        "global_recent_articles": Article.objects.order_by("-created_at")[:3]
    }