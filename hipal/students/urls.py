from django.urls import path, include
from .import views

# Urls patterns for each view
urlpatterns = [
    path('register/', views.RegistrationCreationView.as_view(), name='register'),
    path('enrollment/', views.StudentEnrollmentView.as_view(), name='enrollment'),

]
