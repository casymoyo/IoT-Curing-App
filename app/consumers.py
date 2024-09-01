import json
import re
import asyncio
import serial
from loguru import logger
from . tasks import record_data
from . models import Temperature, Humidity, Stage
from channels.generic.websocket import AsyncWebsocketConsumer
class SerialDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.serial_task = asyncio.create_task(self.read_serial_data())

    async def disconnect(self, close_code):
        if self.serial_task:
            self.serial_task.cancel()

    async def receive(self, text_data):
        # You can handle messages received from WebSocket clients here
        pass

    async def read_serial_data(self):
        try:
            ser = serial.Serial('COM5', 9600, timeout=1)
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').strip()
                    logger.info(f"Received line: {line}")
                    
                    pattern = r"Humidity:\s*(\d+\.\d+)\s*%\s*Temperature:\s*(\d+\.\d+)\s*\*C"
                    match = re.search(pattern, line)
                    
                    if match:
                        humidity = float(match.group(1))
                        temperature = float(match.group(2))
                        
                        data = {
                            "humidity": humidity,
                            "temperature": temperature
                        }
                        
                        # # save the data to the database
                        # await record_data(temperature, humidity)
                
                        await self.send(text_data=json.dumps(data))
                    else:
                        logger.warning(f"Line did not match the expected format: {line}")
                
                await asyncio.sleep(1)  # Non-blocking sleep
        except serial.SerialException as e:
            await self.send(text_data=json.dumps({"error": str(e)}))
        except asyncio.CancelledError:
            ser.close()


