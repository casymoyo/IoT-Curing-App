from django.http import JsonResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Temperature, Humidity
from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html')

def record_data(request):
    if request.method == 'POST':
        temp_value = float(request.POST.get('temperature'))
        humidity_value = float(request.POST.get('humidity'))

        Temperature.objects.create(value=temp_value)
        Humidity.objects.create(value=humidity_value)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "temperature",
            {
                "type": "send_temperature",
                "temperature": temp_value
            }
        )
        async_to_sync(channel_layer.group_send)(
            "humidity",
            {
                "type": "send_humidity",
                "humidity": humidity_value
            }
        )

        return JsonResponse({'status': 'success'}, status=201)
    return JsonResponse({'status': 'failed'}, status=400)
