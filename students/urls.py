from django.urls import path, include
import languages
from .import views
from languages.views import LessonListView

# Urls patterns for each view
urlpatterns = [
    # path('register/', views.RegistrationCreationView.as_view(), name='register'),
    path('enrollment/', views.StudentEnrollmentView.as_view(), name='enrollment'),
    path('lessons/', views.StudentLessonView.as_view(), name='student_lesson_list'),
    path('lesson/<pk>/', views.StudentLessonDetailView.as_view(), name='student_lesson_details'),
    path('lesson/<pk>/unit_id/', views.StudentLessonDetailView.as_view(), name='student_lesson_details_unit'),
    path('', languages.views.LessonListView.as_view(), name='lesson_list'),
    # path('students/login/', views.LoginView.as_view(), name='login'),
    path('accounts/login/login', views.user_login, name='login'),
    path('accounts/students/register/', views.register, name='student_registration'),


]
