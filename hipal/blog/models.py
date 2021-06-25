from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class PublishedPostManager(models.Manager):
    """Custom Blog Post Manager to manage to posts"""

    def get_queryset(self):
        return super(PublishedPostManager, self).get_queryset().filter(status='published')


class BlogPost(models.Model):
    """This is a model to handles any piece of information posted on the blog"""
    # Define all the necessary fields
    CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    blog_body = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=15, choices=CHOICES, default='draft')
    objects = models.Manager()
    published = PublishedPostManager()

    class Meta:
        ordering = ('-published_date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Set canonical url for the blog app"""
        return reverse('blog :blog_post_detail', args=[self.published.year,
                                                       self.published.month,
                                                       self.published.day,
                                                       self.slug])


