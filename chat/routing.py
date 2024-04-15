from django.urls import re_path

from chat.consumers import *

websocket_urlpatterns = [

    re_path(r'api/v1/ws/chat/(?P<room_name>\w+)$', ChatConsumer),
    re_path(r'api/v1/ws/online', ChatConsumer),
    re_path(r'api/v1/ws/offline', ChatConsumer),
    re_path(r'api/v1/ws/refresh_chat_list', ChatConsumer),
]
