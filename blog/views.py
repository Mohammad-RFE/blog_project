from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment, CommentLike
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ArticleForm

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)

    user_liked_comment_ids = []
    if request.user.is_authenticated:
        user_liked_comment_ids = list(
            CommentLike.objects.filter(user=request.user, comment__article=article)
            .values_list('comment_id', flat=True)
        )



    context = {
        'article': article,
        'user_liked_comment_ids': user_liked_comment_ids,
    }
    return render(request, 'blog/post-details.html', context)


def posts_page(request):
    all_sorted_articles = Article.objects.order_by("-created_at")

    search_query = request.GET.get('q')
    tag_slug = request.GET.get('tag')
    category_slug = request.GET.get('category')


    if search_query:
        all_sorted_articles = all_sorted_articles.filter(
            Q(title__icontains=search_query) | Q(body__icontains=search_query)
        )

    elif tag_slug:
        all_sorted_articles = all_sorted_articles.filter(tags__slug=tag_slug)

    elif category_slug:
        all_sorted_articles = all_sorted_articles.filter(category__slug=category_slug)

    paginator = Paginator(all_sorted_articles, 4)
    current_page = request.GET.get('page', 1)
    page_objects = paginator.get_page(current_page)

    context = {
        "articles": page_objects
    }

    return render(request, "blog/blog-entries.html", context)



@login_required
def add_comment(request, article_id):
    if request.method == 'POST':
        article = get_object_or_404(Article, id=article_id)
        body = request.POST.get('body')
        parent_id = request.POST.get('parent_id')

        if body:
            comment = Comment(
                article=article,
                user=request.user,
                body=body
            )

            if parent_id and parent_id.strip() != "" and parent_id != "None":
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment

            comment.save()

        return redirect('article detail', slug=article.slug)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
        comment.delete()
        messages.success(request, "Your comment has been deleted successfully.")
    else:
        redirect("article detail", slug=comment.article.slug)

    return redirect("article detail", slug=comment.article.slug)



@login_required
def like_comment_ajax(request, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=comment_id)
        like_exists = CommentLike.objects.filter(comment=comment, user=request.user)

        if like_exists.exists():
            like_exists.delete()
            liked = False
        else:
            CommentLike.objects.create(comment=comment, user=request.user)
            liked = True

        total_likes = comment.likes.count()

        return JsonResponse({
            "success": True,
            "liked": liked,
            "total_likes": total_likes
        })

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=400)

@login_required
def create_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()

            messages.success(request, "Article created successfully!")
            return redirect('all posts')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ArticleForm()

    context = {
        'form': form,
        'action_title': 'Create New Article'
    }
    return render(request, 'blog/article-form.html', context)


@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if article.author != request.user:
        messages.error(request, "You are not authorized to edit this article.")
        return redirect('all posts')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article updated successfully!")
            return redirect('article detail', slug=article.slug)
    form = ArticleForm(instance=article)

    context = {
        'form': form,
        'article': article,
        'action_title': 'Edit Article'
    }
    return render(request, 'blog/article-form.html', context)


@login_required
def delete_article_cover_ajax(request, article_id):
    if request.method == "POST":
        article = get_object_or_404(Article, id=article_id)

        if article.author != request.user:
            return JsonResponse({"success": False, "error": "Unauthorized"}, status=403)

        if article.cover:
            article.cover.delete(save=False)
            article.cover = None
            article.save()
            return JsonResponse({"success": True, "message": "Cover image deleted successfully."})

        return JsonResponse({"success": False, "error": "No image found."}, status=400)

    return JsonResponse({"success": False, "error": "Bad Request"}, status=400)

@login_required
def delete_article_ajax(request, article_id):
    if request.method == "POST":
        article = get_object_or_404(Article, id=article_id)

        if article.author != request.user:
            return JsonResponse({"success": False, "error": "You are not authorized to delete this article."}, status=403)

        if article.cover:
            article.cover.delete(save=False)

        article.delete()

        return JsonResponse({"success": True, "message": "Article deleted successfully."})

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=400)