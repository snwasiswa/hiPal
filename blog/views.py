from django.shortcuts import render, get_object_or_404
from .models import BlogPost, Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .forms import EmailBlogPostForm, PostCommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count


# Create your views here.
class BlogPostListView(ListView):
    """View for the list of posts"""
    queryset = BlogPost.objects_published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'posts/blog_post_list.html'


def blog_post_list(request, slug_tag=None):
    """View of all the posts"""
    tag = None
    post_list = BlogPost.objects_published.all()

    if slug_tag:
        tag = get_object_or_404(Tag, slug=slug_tag)
        post_list = BlogPost.objects_published.all.filter(tags_in=[tag])
    # Create Paginator object
    paginate_posts = Paginator(post_list, 4)
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
                                                         'page': page,
                                                         'tag': tag})


def blog_post_detail(request, year, month, day, post):
    """Details for a single blog post"""

    blog_post = get_object_or_404(BlogPost, slug=post,
                                  status='published',
                                  published_date__year=year,
                                  published_date__month=month,
                                  published_date__day=day)
    # Comments on the post
    post_comments = blog_post.comments.filter(active=True)
    comment_post = None

    # templatetags ids
    post_ids = blog_post.tags.values_list('id', flat=True)
    # Identical posts
    identical_posts = BlogPost.objects_published.filter(tags__in=post_ids).exclude(id=blog_post.id)
    identical_posts = identical_posts.annotate(same_tags=Count('templatetags')).order_by('-same_tags', '-published_date')[:4]

    if request.method == 'POST':
        # Comment has been posted
        post_comment_form = PostCommentForm(data=request.POST)
        if post_comment_form.is_valid():
            # Create comment object without saving it to database
            comment_post = post_comment_form.save(commit=False)
            comment_post.blog_post = blog_post # Assign current comment to comment
            comment_post.save() # Save to database
    else:
        post_comment_form = PostCommentForm()

    # Return HTTp response
    return render(request, 'posts/blog_post_detail.html', {'post': blog_post,
                                                           'comments': post_comments,
                                                           'comment_post': comment_post,
                                                           'post_comment_form': post_comment_form,
                                                           'identical_posts': identical_posts
                                                           })


def sharing_post(request, blog_post_id):
    """View to handle the sharing posts functionality"""
    blog_post = get_object_or_404(BlogPost, id=blog_post_id, status='published')  # Retrieve posts by id
    send_post = False
    if request.method == 'POST':
        # Form has been submitted
        sharing_form = EmailBlogPostForm(request.POST)
        # Check validation of fields
        if sharing_form.is_valid():
            cd = sharing_form.cleaned_data
            post_url = request.build_absolute_uri(blog_post.get_absolute_url())
            subject = f"You have a recommendation to read {blog_post.title} from {cd['name']}"
            message = f"Read {blog_post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'stewartvas01@gmail.com', [cd['recipients']])
            send_post = True

    else:
        sharing_form = EmailBlogPostForm()

    # Return HTTP response
    return render(request, 'posts/sharing_post.html', {'post': blog_post, 'form': sharing_form, 'sent': send_post})
