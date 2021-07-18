from django.contrib import admin
from django.urls import path, include
from .import views

# Customization of django admin
admin.site.site_header = "hiPal"
admin.site.site_title = "Welcome to hiPal's Dashboard"
admin.site.index_title = "Welcome to the Portal"

# Patterns of different paths
urlpatterns = [
    #path('', views.homepage, name='homepage'),

    path('my_lessons/', views.ManageLessonView.as_view(), name='lessons_list'),
    path('create', views.LessonCreateView.as_view(), name='add_lesson'),
    path('<pk>/edit/', views.LessonUpdateView.as_view(), name='update_lesson'),
    path('<pk>/delete/', views.LessonDeleteView.as_view(), name='delete_lesson'),
    path('<pk>/units/', views.UpdateLessonUnitView.as_view(), name='lessons_units'),
    path('units/<int:unit_id>/content/<model_name>/create_content/', views.CreateContentView.as_view(),
         name='create_unit_content'),
    path('units/<int:unit_id>/content/<model_name>/<id>/', views.CreateContentView.as_view(),
         name='update_unit_content'),
    path('units/<int:unit_id>/delete/', views.DeleteContentView.as_view(), name='delete_unit_content'),
    path('units/<int:unit_id>/', views.ContentListView.as_view(), name='unit_content_list'),
    path('units_order/', views.UnitOrderView.as_view(), name='units_order'),
    path('contents_order/', views.ContentOrderView.as_view(), name='contents_order'),
    path('language/<slug:language>/', views.LessonListView.as_view(), name='lesson_list_language'),
    path('<slug:slug>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('', views.LessonListView.as_view(), name='lesson_list'),

]