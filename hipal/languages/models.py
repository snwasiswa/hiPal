from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderOfField


# Create your models here.
class Language(models.Model):
    """Model to describe language of choice"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Model for the languages"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    creator = models.ForeignKey(User, related_name='lessons_created', on_delete=models.CASCADE, null=True)
    language = models.ForeignKey(Language, related_name='languages', on_delete=models.CASCADE)
    overview = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Module(models.Model):
    language = models.ForeignKey(Lesson, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderOfField(blank=True, for_fields=['languages'])

    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        ordering = ['order']


class Content(models.Model):
    """Model for the type of contents"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': ('video',
                                                                                                            'text',
                                                                                                            'image',
                                                                                                            'file')})
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderOfField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class BaseModel(models.Model):
    """Abstract model that have some fields that some models can inherit from"""
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(User, related_name='%(class) s_related', on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(BaseModel):
    """The Text model has its own fields"""
    content = models.TextField()


class File(BaseModel):
    """This is the model for a file"""
    file = models.FileField(upload_to='files')


class Image(BaseModel):
    """This is the model for a picture"""
    picture = models.FileField(upload_to='images')


class Video(BaseModel):
    """This is the model for a video"""
    file = models.FileField(upload_to='videos')
    url = models.URLField()
