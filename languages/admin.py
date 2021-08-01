from django.contrib import admin
from .models import Language, Lesson, Unit, Profile


# Register your models here.
@admin.register(Language)
class AdminLanguage(admin.ModelAdmin):
    """Register the model with specific fields"""
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class Inline(admin.StackedInline):
    model = Unit


@admin.register(Lesson)
class AdminLesson(admin.ModelAdmin):
    """Register the model with specific fields"""
    list_display = ['title', 'slug', 'created_on', 'creator']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['creator', 'created_on']
    search_fields = ['title', 'outline']
    inlines = [Inline]


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    """Register the model with specific fields"""
    list_display = ['user', 'photo']

# Use memcache admin index site
admin.site.index_template = 'memcache_status/admin_index.html'
