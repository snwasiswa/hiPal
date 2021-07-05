from django.shortcuts import render, get_object_or_404
from .models import BlogPost
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def blog_post_list(request):
    """Views for all the posts"""
    # Create Paginator object
    paginate_posts = Paginator(BlogPost.objects_published.all(), 3)
    page = request.GET.get('page')
    try:
        posts = paginate_posts.page(page)
    except PageNotAnInteger:
        # Deliver the first page
        posts = paginate_posts.page(1)
    except EmptyPage:
        # Deliver last page
        posts = paginate_posts.page(paginate_posts.num_pages)

    # Return HTTP response
    return render(request, 'posts/blog_post_list.html', {'posts': posts,
                                                         'page': page})


def blog_post_detail(request, year, month, day, post):
    """Details for a single blog post"""
    # Return HTTp response
    return render(request, 'posts/blog_post_detail.html', {'post': get_object_or_404(BlogPost, slug=post,
                                                                                     status='published',
                                                                                     published_date__year=year,
                                                                                     published_date__month=month,
                                                                                     published_date__day=day)})
