from django.contrib import admin
from .models import BlogPost, Comment


# Register your models here.
@admin.register(BlogPost)
class BlogPostAdminCustomization(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug', 'published_date', 'status')
    search_fields = ('title','author','blog_body')
    list_filter = ('title','author','status','published_date')
    prepopulated_fields = {'slug':('title',)}
    date_hierarchy = 'published_date'
    raw_id_fields = ('author',)
    ordering = ('published_date','status')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'blog_post', 'created_date', 'active')
    search_fields = ('name','email','body')
    list_filter = ('active','created_date', 'updated_date')
