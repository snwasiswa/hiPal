from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

from blog.models import BlogPost

register = template.Library()


@register.simple_tag
def total_posts():
    """ Custom tag for the total number of blog posts"""
    return BlogPost.objects_published.count()


@register.inclusion_tag('posts/latest_posts.html')
def latest_posts(count=6):
    """Custom tag for the latest posts"""
    return {'latest_posts': BlogPost.objects_published.order_by('-published_date')[:count]}


@register.simple_tag
def most_commented_posts(count=6):
    """Custom tag for the most commented posts"""
    return BlogPost.objects_published.annotate(comments_number=Count('comments')).order_by('-comments_number')[:count]


@register.filter(name='markdown')
def custom_markdown(text):
    """Custom template filter to markdown posts"""
    return mark_safe(markdown.markdown(text))
