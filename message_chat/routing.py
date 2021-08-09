from django.urls import re_path
from .import consumers

messaging_urlpatterns = [
    re_path(r'ws/messaging/room/(?P<lesson_id>\d+)/$', consumers.Consumer.as_asgi()),
]