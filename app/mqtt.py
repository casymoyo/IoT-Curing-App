import paho.mqtt.client as mqtt
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'curing_backend.settings')
application = get_wsgi_application()

from models import Temperature, Humidity  

MQTT_BROKER_URL = 'mqtt://mqtt:1883'  
channel_layer = get_channel_layer()

def on_connect(client, userdata, flags, rc):
    client.subscribe('temperature')
    client.subscribe('humidity')

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = float(msg.payload.decode())

    if topic == 'temperature':
        
        Temperature.objects.create(value=payload)

        async_to_sync(channel_layer.group_send)(
            "temperature",
            {
                "type": "send_temperature",
                "temperature": payload
            }
        )
    elif topic == 'humidity':
        Humidity.objects.create(value=payload)

        async_to_sync(channel_layer.group_send)(
            "humidity",
            {
                "type": "send_humidity",
                "humidity": payload
            }
        )

def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER_URL, 1883, 60)
    client.loop_start()
