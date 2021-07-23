from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'languages'
# Build url dynamically using router
router = routers.DefaultRouter()
router.register(app_name, views.LessonViewSet)

# Patterns of different paths for the API
urlpatterns = [

    path('languages/', views.LanguageListView.as_view(), name='list'),
    path('languages/<pk>/', views.LanguageDetailView.as_view(), name='details'),
    path('lessons/<lesson_id>/enrollment/', views.LessonEnrollmentView.as_view(), name='enrollment'),
    path('api/', include(router.urls)),

]
