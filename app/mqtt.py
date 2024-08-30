import paho.mqtt.client as mqtt
import os
import django
from django.conf import settings
from loguru import logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'curing_backend.settings')
django.setup()

from . models import Temperature, Humidity

MQTT_BROKER = os.getenv('MQTT_BROKER', 'mqtt_broker')  
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'tobacco/#')

def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

# Callback when a message is received
def on_message(client, userdata, msg):
    logger.info("Topic: {msg.topic}\nMessage: {msg.payload.decode()}")
    
    if 'temperature' in msg.topic:
        temperature = float(msg.payload.decode())
        Temperature.objects.create(value=temperature)
    elif 'humidity' in msg.topic:
        humidity = float(msg.payload.decode())
        Humidity.objects.create(value=humidity)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_start()
