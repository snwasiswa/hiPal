from django.contrib import admin
from .models import Language, Lesson, Module, Content

# Register your models here.

@admin.register(Language)
class AdminLanguage(admin.ModelAdmin):
    """Register the model with specific fields"""
    list_display = ['title','slug']
    prepopulated_fields = {'slug':('title',)}

class Inline(admin.StackedInline):
    model = Module

@admin.register(Lesson)
class AdminLesson(admin.ModelAdmin):
    """Register the model with specific fields"""
    list_display = ['title','slug', 'created_on','creator']
    prepopulated_fields = {'slug':('title',)}
    list_filter = ['creator', 'created_on']
    search_fields = ['title', 'overview']
    inlines = [Inline]
