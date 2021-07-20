from django.urls import path, include
from .import views

# Urls patterns for each view
urlpatterns = [
    path('register/', views.RegistrationCreationView.as_view(), name='register'),
    path('enrollment/', views.StudentEnrollmentView.as_view(), name='enrollment'),
    path('lessons/', views.StudentLessonView.as_view(), name='student_lesson_list'),
    path('lesson/<pk>/', views.StudentLessonDetailView.as_view(), name='student_lesson_details'),
    path('lesson/<pk>/unit_id/', views.StudentLessonDetailView.as_view(), name='student_lesson_details_unit'),


]
