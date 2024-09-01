from utils.email import EmailThread
from django.core.mail import EmailMessage
from loguru import logger
from django.shortcuts import get_object_or_404
from . models import *
from django.utils import timezone

def send_end_of_day_report(buffer):
    email = EmailMessage(
        f"End of Day Report:",
        "Please find the attached End of Day report. The expected amount is to be calculated on cost price, since they are no stipulated prices per dishes, but if they to be put the expected table will be relavant.",
        'admin@techcity.co.zw',
        ['cassymyo@gmail.com'],
    )
    email.attach(f'EndOfDayReport.pdf', buffer.getvalue(), 'application/pdf')
    
    EmailThread(email).start()

    logger.info(f' End of day report email sent.')
    

def record_data(temp_value, humidity_value):
    
    current_stage = get_object_or_404(Stage, selected=True)
    
    temperature = Temperature.objects.create(value=temp_value, stage=current_stage)
    humidity = Humidity.objects.create(value=humidity_value, stage=current_stage)
    
    temp_config = get_object_or_404(Config, stage=current_stage, name=Config.NameChoices.TEMPERATURE)
    humidity_config = get_object_or_404(Config, stage=current_stage, name=Config.NameChoices.HUMIDITY)
    
    temp_status = ''
    temp_description = ''
    
    if temperature.value < temp_config.lower_limit_value:
        if temperature.value >= temp_config.lower_limit_value - 5:
            temp_status = AlertLog.AlertType.LOW
            temp_description = 'Low temperature'
        else:
            temp_status = AlertLog.AlertType.MID
            temp_description = 'Very low temperature'
    else:
        temp_status = AlertLog.AlertType.HIGH
        temp_description = 'High temperature'

    temp_alert_log = AlertLog.objects.create(
        timestamp=timezone.now(),
        description=temp_description,
        alert_type=temp_status,
        stage=current_stage
    )
    
    humidity_status = ''
    humidity_description = ''

    if humidity.value < humidity_config.lower_limit_value:
        if humidity.value >= humidity_config.lower_limit_value - 5:
            humidity_status = AlertLog.AlertType.LOW
            humidity_description = 'Low humidity'
        else:
            humidity_status = AlertLog.AlertType.MID
            humidity_description = 'Very low humidity'
    else:
        humidity_status = AlertLog.AlertType.HIGH
        humidity_description = 'High humidity'

    humidity_alert_log = AlertLog.objects.create(
        timestamp=timezone.now(),
        description=humidity_description,
        alert_type=humidity_status,
        stage=current_stage
    )
    
    if temp_alert_log:
        logger.info(f'{temp_alert_log} logged')
    
    if humidity_alert_log:
        logger.info(f'{humidity_alert_log} logged')
        

    logger.info('Data successfully recorded')