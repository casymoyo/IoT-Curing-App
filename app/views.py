from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Stage, Temperature, Humidity, Config, AlertLog
from .serializers import StageSerializer, TemperatureSerializer, HumiditySerializer, ConfigSerializer, AlertLogSerializer

from django.http import HttpResponse
from .tasks import add

def test_task(request):
    result = add.delay(10, 20)
    return HttpResponse(f'Task result: {result.get(timeout=1)}')

class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer

class TemperatureViewSet(viewsets.ModelViewSet):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer

    @action(detail=False, methods=['post'])
    def record(self, request):
        temp_value = float(request.data.get('temperature'))
        timestamp = timezone.now()
        temperature = Temperature.objects.create(value=temp_value, timestamp=timestamp)
        serializer = self.get_serializer(temperature)
        return Response(serializer.data, status=201)

class HumidityViewSet(viewsets.ModelViewSet):
    queryset = Humidity.objects.all()
    serializer_class = HumiditySerializer

    @action(detail=False, methods=['post'])
    def record(self, request):
        humidity_value = float(request.data.get('humidity'))
        timestamp = timezone.now()
        humidity = Humidity.objects.create(value=humidity_value, timestamp=timestamp)
        serializer = self.get_serializer(humidity)
        return Response(serializer.data, status=201)

class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer

class AlertLogViewSet(viewsets.ModelViewSet):
    queryset = AlertLog.objects.all()
    serializer_class = AlertLogSerializer
    


