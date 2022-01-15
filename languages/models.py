from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from .fields import OrderOfField
from django.conf import settings


# Create your models here.
class Language(models.Model):
    """Model to describe language of choice"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(blank=True, null=True, upload_to="logos")

    class Meta:
        app_label = 'languages'
        ordering = ['title']

    def __str__(self):
        return self.title

    @property
    def get_logo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "https://res.cloudinary.com/dh13i9dce/image/upload/v1642216413/media/logos/default-thumb_dn1xzg.png"


class Lesson(models.Model):
    """Model for the languages"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    creator = models.ForeignKey(User, related_name='lessons_created', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, related_name='lessons', on_delete=models.CASCADE)
    outline = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    student = models.ManyToManyField(User, related_name='lessons_joined', blank=True)

    class Meta:
        app_label = 'languages'
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Unit(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='units', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderOfField(blank=True, for_fields=['lesson'])

    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        app_label = 'languages'
        ordering = ['order']


class Content(models.Model):
    """Model for the type of contents"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': ('video',
                                                                                                            'text',
                                                                                                            'image',
                                                                                                            'file')})
    unit = models.ForeignKey(Unit, related_name='contents', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderOfField(blank=True, for_fields=['unit'])

    class Meta:
        app_label = 'languages'
        ordering = ['order']


class BaseModel(models.Model):
    """Abstract model that have some fields that some models can inherit from"""
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(User, related_name='%(class) s_related', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'languages'
        abstract = True

    def render(self):
        """Renders dynamically generated templates and returns contents as a string"""
        return render_to_string(f'contents/{self._meta.model_name}.html', {'item': self})

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


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(default='default.jpg', upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'
