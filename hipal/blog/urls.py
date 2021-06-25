from django.contrib import admin
from django.urls import path, include
from .import views

# Patterns of different paths
urlpatterns = [
    path('', views.blog_post_list, name='blog_post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.blog_post_detail, name='blog_post_detail'),
]