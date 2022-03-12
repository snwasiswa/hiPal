from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


# Create your models here.
class PublishedPostManager(models.Manager):
    """Custom Blog Post Manager to manage posts"""

    class Meta:
        app_label = 'blog'

    def get_queryset(self):
        return super(PublishedPostManager, self).get_queryset().filter(status='published')


class BlogPost(models.Model):
    """This is a model to handles any piece of information posted on the blog"""
    # Define all the necessary fields
    CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='published_date')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    blog_body = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=15, choices=CHOICES, default='draft')
    objects = models.Manager()
    objects_published = PublishedPostManager()
    tags = TaggableManager()

    class Meta:
        app_label = 'blog'
        ordering = ('-published_date',)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Set canonical url for the blog app"""
        return reverse('blog:blog_post_detail', args=[self.published_date.year,
                                                      self.published_date.month,
                                                      self.published_date.day,
                                                      self.slug])


class Comment(models.Model):
    """Model for the comments on posts"""
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    body = RichTextField()
    email = models.EmailField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        app_label = 'blog'
        ordering = ('created_date', )

    def __str__(self):
        return f"Commented by {self.name} on {self.blog_post}"

