from django.urls import path
from .import views

# Urls patterns for each view
urlpatterns = [
    path('register/', views.RegistrationCreationView.as_view(), name='register'),

]
