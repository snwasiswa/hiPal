from django.urls import path
from . import views

app_name = 'languages'

# Patterns of different paths for the API
urlpatterns = [

    path('languages/', views.LanguageListView.as_view(), name='list'),
    path('languages/<pk>/', views.LanguageDetailView.as_view(), name='details'),
    path('lessons/<lesson_id>/enrollment/', views.LessonEnrollmentView.as_view(), name='enrollment'),

]
