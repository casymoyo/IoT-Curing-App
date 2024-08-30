from django.test import TestCase
from django.urls import reverse
from users.models import User
from django.utils import timezone
from .models import Humidity, Temperature, Config, Stage, AlertLog

class TemperatureModelTests(TestCase):
    def setUp(self):
        self.temperature = Temperature.objects.create(value=25.0)

    def test_temperature_creation(self):
        self.assertEqual(self.temperature.value, 25.0)
    
    def test_temperature_list_view(self):
        response = self.client.get(reverse('temperature-list'))
        self.assertEqual(response.status_code, 200)

class HumidityModelTests(TestCase):
    def setUp(self):
        self.humidity = Humidity.objects.create(value=25.0)
    
    def test_humidity_creation(self):
        self.assertEqual(self.humidity.value, 25.0)
    
    def test_humidity_list_view(self):
        response = self.client.get(reverse('humidity-list'))
        self.assertEqual(response.status_code, 200)
        

class ConfigModelTests(TestCase):
    def setUp(self):
        self.stage = Stage.objects.create(name=Stage.StageChoices.INITIAL)
        self.user = User.objects.create_user(username='user', password='password')

    def test_config_creation(self):
        config = Config.objects.create(
            stage=self.stage,
            name=Config.NameChoices.TEMPERATURE,
            lower_limit_value=22.5,
            upper_limit_value=30.5,
            user=self.user
        )
        
        fetched_config = Config.objects.get(id=config.id)

        self.assertEqual(fetched_config.stage, self.stage)
        self.assertEqual(fetched_config.name, Config.NameChoices.TEMPERATURE)
        self.assertEqual(fetched_config.lower_limit_value, 22.5)
        self.assertEqual(fetched_config.upper_limit_value, 30.5)
        self.assertEqual(fetched_config.user, self.user)
    
    def test_config_update(self):
        config = Config.objects.create(
            stage=self.stage,
            name=Config.NameChoices.TEMPERATURE,
            lower_limit_value=22.5,
            upper_limit_value=30.5,
            user=self.user
        )
        
        config.lower_limit_value = 20.0
        config.upper_limit_value = 35.0
        config.save()

        updated_config = Config.objects.get(id=config.id)

        self.assertEqual(updated_config.lower_limit_value, 20.0)
        self.assertEqual(updated_config.upper_limit_value, 35.0)
        

    def test_config_list_view(self):
        response = self.client.get(reverse('config-list'))
        self.assertEqual(response.status_code, 200)
        
class AlertLogsModelTests(TestCase):
    def setUp(self):
        self.temperature = Temperature.objects.create(value=25.0)
        self.stage = Stage.objects.create(name=Stage.StageChoices.INITIAL)
        self.user = User.objects.create_user(username='user', password='password')
        
        self.config = Config.objects.create(
            stage=self.stage,
            name=Config.NameChoices.TEMPERATURE,
            lower_limit_value=22.5,
            upper_limit_value=30.5,
            user=self.user
        )
        
    def test_alert_logs_creation(self):
        status = ''
        description = ''
        
        if self.config.stage == self.stage:
            if self.temperature.value < self.config.lower_limit_value:
                if self.temperature.value >= self.config.lower_limit_value - 5:
                    status = AlertLog.AlertType.LOW
                else:
                    status = AlertLog.AlertType.MID
                description = 'low temp'
            else:
                status = AlertLog.AlertType.HIGH
                description = 'high temp'

        log = AlertLog.objects.create(
            timestamp=timezone.now(),
            description=description,
            alert_type=status
        )
        
        fetched_log = AlertLog.objects.get(id=log.id)

        self.assertEqual(fetched_log.alert_type, status)
        self.assertEqual(fetched_log.description, description)
        self.assertTrue(fetched_log.timestamp)
        
      
        
            
        


