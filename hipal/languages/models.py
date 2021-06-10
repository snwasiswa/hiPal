from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Language(models.Model):
    """Model to describe language of choice"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length = 200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Lesson(models.Model):
    """Model for the lesson"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length = 200, unique=True)
    creator = models.ForeignKey(User, related_name='lessons_created', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, related_name = 'lessons', on_delete=models.CASCADE)
    overview = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.title

class Module (models.Model):
    language = models.ForeignKey(Lesson, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Content(models.Model):
    """Model for the type of contents"""
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    module = models.ForeignKey(Module, related_name='contents',on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
