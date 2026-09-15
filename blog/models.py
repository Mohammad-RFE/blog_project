# Models for handling tags, categories, articles, comments, and likes
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from blog_project.settings import AUTH_USER_MODEL
from PIL import Image, ImageOps

class Tag(models.Model):
    """
    Represents a tag/keyword associated with blog articles.
    """
    objects = None
    title = models.CharField(unique=True, max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Automatically generate slug from title if not set
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Category(models.Model):
    """
    Represents a topic category for organizing articles.
    """
    objects = None
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Automatically generate slug from title if not set
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Article(models.Model):
    """
    Represents a blog post with media support, categorization, and tags.
    """
    objects = None
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to="article_covers", null=True, blank=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Automatically generate slug from title if not set
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        # Resize and crop the uploaded cover image to standard dimensions (520x450)
        if self.cover and self.cover.name:
            try:
                img_path = self.cover.path
                img = Image.open(img_path)

                target_width = 520
                target_height = 450

                resized_img = ImageOps.fit(img, (target_width, target_height), Image.Resampling.LANCZOS)
                resized_img.save(img_path, quality=90)
            except ValueError:
                pass


class Comment(models.Model):
    """
    Represents a comment or nested reply on an article.
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Self-referential relation for nested reply functionality
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment from {self.user.username} on Article {self.article.title}--{self.body[:30]}"


class CommentLike(models.Model):
    """
    Tracks unique likes given by users to comments.
    """
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent multiple likes on the same comment by the same user
        unique_together = ('comment', 'user')

    def __str__(self):
        return f"{self.user.username} liked {self.comment.id}"