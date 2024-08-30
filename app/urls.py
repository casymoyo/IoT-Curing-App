from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StageViewSet, 
    TemperatureViewSet, 
    HumidityViewSet, 
    ConfigViewSet, 
    AlertLogViewSet,
    test_task
)

router = DefaultRouter()
router.register(r'stages', StageViewSet)
router.register(r'temperatures', TemperatureViewSet)
router.register(r'humidity', HumidityViewSet)
router.register(r'configs', ConfigViewSet)
router.register(r'alert-logs', AlertLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test-task/', test_task, name='test_task'),
]
