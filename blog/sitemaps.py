from django.contrib.sitemaps import Sitemap
from .models import BlogPost


class BlogPostSitemap(Sitemap):
    """Custom class for sitemaps"""
    frequency = 'weekly'
    priority = 0.9

    def items(self):
        """Returns queryset of objects"""
        return BlogPost.objects_published.all()

    def last_modification(self, object):
        """Returns the last time an object was modified"""
        return object.updated