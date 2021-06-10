from django.contrib import admin
from django.urls import path, include
from languages import views

# Customization of django admin
admin.site.site_header = "hiPal"
admin.site.site_title = "Welcome to hiPal's Dashboard"
admin.site.index_title = "Welcome to the Portal"

urlpatterns = [
    path('', views.homepage, name='homepage'),
]