from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from .models import BlogPost
from django.template.defaultfilters import truncatewords


class BlogPostFeed(Feed):
    """Feed for the latest blog post"""
    title = 'Blog'
    description = 'New blog posts.'
    link = reverse_lazy('blog:blog_post_list')

    def items(self):
        return BlogPost.objects_published.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.blog_body, 40)