# Context processor to expose sidebar data across all templates
from .models import Category, Tag, Article

def sidebar(request):
    """
    Injects global sidebar data including categories, tags, and latest articles into all template contexts.
    """
    return {
        "global_categories": Category.objects.all(),
        "global_tags": Tag.objects.all(),
        "global_recent_articles": Article.objects.order_by("-created_at")[:3]
    }