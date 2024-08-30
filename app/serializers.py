from rest_framework import serializers
from .models import Stage, Temperature, Humidity, Config, AlertLog

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'

class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = '__all__'

class HumiditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Humidity
        fields = '__all__'

class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = '__all__'

class AlertLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertLog
        fields = '__all__'
