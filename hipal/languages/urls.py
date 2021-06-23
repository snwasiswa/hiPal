from django.contrib import admin
from django.urls import path, include
from .import views

# Customization of django admin
admin.site.site_header = "hiPal"
admin.site.site_title = "Welcome to hiPal's Dashboard"
admin.site.index_title = "Welcome to the Portal"

# Patterns of different paths
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('mine/', views.ManageLessonView.as_view(), name='manage_lesson_list'),
    path('create', views.LessonCreateView.as_view(), name='lesson_create'),
    path('<pk>/edit/', views.LessonUpdateView.as_view(), name='lesson_edit'),
    path('<pk>/delete/', views.LessonDeleteView.as_view(), name='lesson_delete'),

]