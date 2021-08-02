from django.urls import path
from .import views

app_name = 'message_chat'

# Urls patterns for each view
urlpatterns = [

    path('chat/<int:pk>/', views.chat, name='chat'),

]
