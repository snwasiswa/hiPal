"""hipal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import BlogPostSitemap
import languages
from languages.views import custom_logout_view

sitemaps = {
    'posts': BlogPostSitemap,
}


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('languages.urls')),
                  path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
                  # path('accounts/login/', views.LoginView.as_view(), name='login'),
                  # path('accounts/logout/', languages.views.custom_logout_view, name='logout'),
                  path('accounts/logout/', views.LogoutView.as_view(template_name='registration/logout.html'),
                       name='logout'),
                  path('', include('students.urls')),
                  path('messaging/', include('message_chat.urls', namespace='message_chat')),
                  path('restapi/', include('languages.restapi.urls', namespace='restapi')),
                  path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
                  path('social-auth/', include('social_django.urls', namespace='social-auth')),


                  # path('accounts/', include('django.contrib.auth.urls')),
                  # path('', TemplateView.as_view(template_name='registration/studentlogin.html'), name='login'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
