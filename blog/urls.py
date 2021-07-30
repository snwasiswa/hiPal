from django.contrib import admin
from django.urls import path, include
from . import views
from .feeds import BlogPostFeed

# Patterns of different paths
urlpatterns = [
    # path('', views.BlogPostListView.as_view(), name='blog_post_list'),
    path('', views.blog_post_list, name='blog_post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.blog_post_detail, name='blog_post_detail'),
    path('<int:blog_post_id>/sharing/', views.sharing_post, name='sharing_post'),
    path('tag/<slug:slug_tag>/', views.blog_post_list, name='blog_post_list_with_tag'),
    path('feed/', BlogPostFeed(), name='feed'),
    path('search/', views.search_engine, name='search_post'),

]
