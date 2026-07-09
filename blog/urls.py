from django.urls import path
from . import views

urlpatterns = [
    path("article-detail/<slug:slug>", views.article_detail, name="article detail"),
    path("all-posts/", views.posts_page, name="all posts"),
    path('article/<int:article_id>/comment/add/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('article/create/', views.create_article, name='create_article'),
    path('article/<int:article_id>/edit/', views.edit_article, name='edit_article'),
    path('article/<int:article_id>/delete-cover/', views.delete_article_cover_ajax, name='delete_article_cover'),
    path('article/<int:article_id>/delete/', views.delete_article_ajax, name='delete_article'),
    path('comment/<int:comment_id>/like/', views.like_comment_ajax, name='like_comment_ajax'),
]