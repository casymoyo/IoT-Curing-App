from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/serial-data/', consumers.SerialDataConsumer.as_asgi()),
]
