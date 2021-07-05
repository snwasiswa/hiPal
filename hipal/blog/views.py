from django.shortcuts import render, get_object_or_404
from .models import BlogPost


# Create your views here.
def blog_post_list(request):
    """Views for all the posts"""
    # Return HTTP response
    return render(request, 'posts/blog_post_list.html', {'posts': BlogPost.objects_published.all()})


def blog_post_detail(request, year, month, day, post):
    """Details for a single blog post"""
    # Return HTTp response
    return render(request, 'posts/blog_post_detail.html', {'post': get_object_or_404(BlogPost, slug=post,
                                                                                     status='published',
                                                                                     year_of_publication=year,
                                                                                     month_of_publication=month,
                                                                                     day_of_publication=day)})
