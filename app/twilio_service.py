from twilio.rest import Client
from loguru import logger

def send_whatsapp_message(to_number, message_body):
    client = Client('', '')
    logger.info(client)
    message = client.messages.create(
        body=message_body,
        from_='',
        to=f'whatsapp:{to_number}'
    )
    
    return message
