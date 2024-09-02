from twilio.rest import Client
from loguru import logger

def send_whatsapp_message(to_number, message_body):
    client = Client('AC66182987c24e7793940afb3d14f1b733', '616a8c6652882e0e3af9b7a442f76c20')
    logger.info(client)
    message = client.messages.create(
        body=message_body,
        from_='whatsapp:+14155238886',
        to=f'whatsapp:{to_number}'
    )
    
    return message
