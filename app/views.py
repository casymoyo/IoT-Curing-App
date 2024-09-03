import json
from django.http import JsonResponse
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Temperature, Humidity, AlertLog, Config, Stage
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from .models import Config
from .forms import ConfigForm 
from django.views.decorators.http import require_http_methods
from loguru import logger
from django.db.models import Count, Avg, Q
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from utils.serial import read_serial_data 
from django.db.models.functions import ExtractHour
from twilio.rest import Client
from .twilio_service import send_whatsapp_message

def update_stage(request):
    if request.method == 'POST':
        stage_id = request.POST.get('stage_id')

        if not stage_id:
            return JsonResponse({'status': 'failed', 'message': 'Stage ID is required'}, status=400)
        
        Stage.objects.update(selected=False)

        stage = get_object_or_404(Stage, id=stage_id)
        stage.selected = True
        stage.save()

        return JsonResponse({'status': 'success', 'selected_stage': stage.name}, status=200)
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)

def dashboard(request):
    stages = Stage.objects.all()
    return render(request, 'dashboard.html', {'stages':stages})

def alert_log_data(request):
    logs = AlertLog.objects.all().values(
        'timestamp',
        'description',
        'stage__name',
        'alert_type'
    )
    return JsonResponse(list(logs), safe=False)


def serial_data_view(request):
    data = read_serial_data()
    logger.info(data)
    if "Error" in data:
        return JsonResponse({'status': 'error', 'message': data}, status=500)
    return JsonResponse({'status': 'success', 'data': data})


def alert_log_list(request):
    if request.method == 'GET':
        logs = list(AlertLog.objects.values('timestamp', 'type', 'description'))
        return JsonResponse(logs, safe=False)

def record_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            temperature = float(data.get('temperature'))
            humidity = float(data.get('humidity'))

            current_stage = get_object_or_404(Stage, selected=True)
            logger.info(current_stage)

            Temperature.objects.create(value=temperature, stage=current_stage)
            Humidity.objects.create(value=humidity, stage=current_stage)

            temp_config = get_object_or_404(Config, stage=current_stage, name=Config.NameChoices.TEMPERATURE)
            humidity_config = get_object_or_404(Config, stage=current_stage, name=Config.NameChoices.HUMIDITY)

            temp_status = ''
            temp_description = ''

            if temperature < temp_config.lower_limit_value:
                if temperature >= temp_config.lower_limit_value - 5:
                    temp_status = AlertLog.AlertType.LOW
                    temp_description = 'Low temperature'
                else:
                    temp_status = AlertLog.AlertType.MID
                    temp_description = 'Very low temperature'
            else:
                temp_status = AlertLog.AlertType.HIGH
                temp_description = 'High temperature'

            AlertLog.objects.create(
                timestamp=timezone.now(),
                description=temp_description,
                alert_type=temp_status,
                stage=current_stage
            )

            humidity_status = ''
            humidity_description = ''

            if humidity < humidity_config.lower_limit_value:
                if humidity >= humidity_config.lower_limit_value - 5:
                    humidity_status = AlertLog.AlertType.LOW
                    humidity_description = 'Low humidity'
                else:
                    humidity_status = AlertLog.AlertType.MID
                    humidity_description = 'Very low humidity'
            else:
                humidity_status = AlertLog.AlertType.HIGH
                humidity_description = 'High humidity'

            AlertLog.objects.create(
                timestamp=timezone.now(),
                description=humidity_description,
                alert_type=humidity_status,
                stage=current_stage
            )
            
            try:
                if temp_status in [AlertLog.AlertType.MID, AlertLog.AlertType.HIGH]:
                    send_whatsapp_message(
                        '+263717773066',  # Recipient number
                        f"Temperature Alert: {temp_description} - {temperature}°C"
                    )

                if humidity_status in [AlertLog.AlertType.MID, AlertLog.AlertType.HIGH]:
                    send_whatsapp_message(
                        '+263717773066',  # Recipient number
                        f"Humidity Alert: {humidity_description} - {humidity}%"
                    )
            except Exception as e:
                logger.info(f'whatsapp twilio: {e}')
                
            return JsonResponse({'status': 'success'}, status=201)
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'failed'}, status=400)


def config_list(request):
    configs = Config.objects.all()
    return render(request, 'config_list.html', {'object_list': configs})


@require_http_methods(["GET", "POST"])
def config_create(request):
    if request.method == 'POST':
        form = ConfigForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuration created successfully.')
            return redirect(reverse('config-list'))
    else:
        form = ConfigForm()
    
    return render(request, 'config_form.html', {'form': form})


@require_http_methods(["GET", "POST"])
def config_update(request, pk):
    config = get_object_or_404(Config, pk=pk)
    if request.method == 'POST':
        form = ConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuration updated successfully.')
            return redirect(reverse('config-list'))
    else:
        form = ConfigForm(instance=config)
    
    return render(request, 'config_form.html', {'form': form})


@require_http_methods(["POST"])
def config_delete(request, pk):
    config = get_object_or_404(Config, pk=pk)
    if request.method == 'POST':
        config.delete()
        messages.success(request, 'Configuration deleted successfully.')
        return redirect(reverse('config-list'))
    return HttpResponseForbidden("Invalid request")


def report_data(request):
    filter_time = request.GET.get('filter_time', 'today')
    now = timezone.now()

    if filter_time == 'today':
        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif filter_time == 'week':
        start_time = now - timedelta(days=now.weekday())
        start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
    elif filter_time == 'month':
        start_time = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif filter_time == 'year':
        start_time = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        return JsonResponse({'error': 'Invalid filter_time parameter'}, status=400)

    logger.info(f"Fetching data from {start_time} to {now}")

    try:
       
        temperature_data = get_hourly_average(Temperature, start_time, now)
        humidity_data = get_hourly_average(Humidity, start_time, now)

        temperature_stage_averages = get_stage_averages(Temperature, start_time, now)
        humidity_stage_averages = get_stage_averages(Humidity, start_time, now)

        alerts_by_day = AlertLog.objects.filter(timestamp__gte=start_time).values('timestamp__date').annotate(alert_count=Count('id')).order_by('-alert_count')
        top_alert_day = alerts_by_day.first() if alerts_by_day else {}

        response_data = {
            'temperature_data': temperature_data,
            'humidity_data': humidity_data,
            'temperature_stage_averages': temperature_stage_averages,
            'humidity_stage_averages': humidity_stage_averages,
            'top_alert_day': top_alert_day
        }
        
        logger.info(f"Data fetched successfully")
        return JsonResponse(response_data)

    except ObjectDoesNotExist as e:
        logger.error(f"Database query failed: {str(e)}")
        return JsonResponse({'error': 'Data not found'}, status=404)
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

def get_hourly_average(model, start_time, end_time):
    data = model.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time)\
        .annotate(hour=ExtractHour('timestamp'))\
        .values('hour')\
        .annotate(average_value=Avg('value'))\
        .order_by('hour')

    hourly_data = {hour: {'hour': hour, 'average_value': None} for hour in range(24)}
    for item in data:
        hourly_data[item['hour']] = {
            'hour': item['hour'],
            'average_value': round(item['average_value'], 2) if item['average_value'] is not None else None
        }

    return list(hourly_data.values())

def get_stage_averages(model, start_time, end_time):
    stage_data = model.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time)\
        .values('stage')\
        .annotate(
            initial_avg=Avg('value', filter=Q(timestamp__hour__lt=8)),
            mid_avg=Avg('value', filter=Q(timestamp__hour__gte=8, timestamp__hour__lt=16)),
            final_avg=Avg('value', filter=Q(timestamp__hour__gte=16))
        )

    return {
        item['stage']: {
            'initial_avg': round(item['initial_avg'], 2) if item['initial_avg'] is not None else None,
            'mid_avg': round(item['mid_avg'], 2) if item['mid_avg'] is not None else None,
            'final_avg': round(item['final_avg'], 2) if item['final_avg'] is not None else None,
        }
        for item in stage_data
    }

def report_view(request):
    now = timezone.now()
    filter_time = request.GET.get('filter_time', '5min')
    
    if filter_time == 'week':
        start_time = now - timedelta(weeks=1)
    elif filter_time == 'month':
        start_time = now - timedelta(days=30)
    elif filter_time == 'year':
        start_time = now - timedelta(days=365)
    else:  # Default to last 5 minutes
        start_time = now - timedelta(minutes=5)

    temperature_data = Temperature.objects.filter(timestamp__gte=start_time)
    humidity_data = Humidity.objects.filter(timestamp__gte=start_time)

    # Aggregate alerts by day
    alerts_by_day = AlertLog.objects.filter(timestamp__gte=start_time).values('timestamp__date').annotate(alert_count=Count('id')).order_by('-alert_count')
    top_alert_day = alerts_by_day.first() if alerts_by_day else {}

    context = {
        'temperature_data': temperature_data,
        'humidity_data': humidity_data,
        'top_alert_day': top_alert_day,
        'filter_time': filter_time,
    }

    return render(request, 'report.html', context)

def download_report(request):
    filter_time = request.GET.get('filter_time', '5min')
    now = timezone.now()

    if filter_time == 'week':
        start_time = now - timedelta(weeks=1)
    elif filter_time == 'month':
        start_time = now - timedelta(days=30)
    elif filter_time == 'year':
        start_time = now - timedelta(days=365)
    else:
        start_time = now - timedelta(minutes=5)

    temperature_data = Temperature.objects.filter(timestamp__gte=start_time)
    humidity_data = Humidity.objects.filter(timestamp__gte=start_time)
    
    import csv
    from django.http import HttpResponse

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="report_{filter_time}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Timestamp', 'Temperature', 'Humidity'])

    for temp, hum in zip(temperature_data, humidity_data):
        writer.writerow([temp.timestamp, temp.value, hum.value])

    return response


