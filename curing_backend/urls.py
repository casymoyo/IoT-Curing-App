from django.contrib import admin
from django.urls import path, include, re_path
from app.routing import websocket_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('app.urls')),
    path('users/', include('users.urls', namespace='users')),
    re_path(r'ws/', include(websocket_urlpatterns)),
]
