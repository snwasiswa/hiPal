from django.contrib.sitemaps import Sitemap
from .models import BlogPost


class BlogPostSitemap(Sitemap):
    """Custom class for sitemaps"""
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        """Returns queryset of objects"""
        return BlogPost.objects_published.all()

    def lastmod(self, object):
        """Returns the last time an object was modified"""
        return object.updated_date