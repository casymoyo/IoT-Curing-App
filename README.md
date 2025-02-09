# Tobacco Curing IoT App

This is a Django-based IoT application designed to monitor and control the tobacco curing process. The system connects to a **DHT11 sensor** to capture real-time temperature and humidity readings. Using **WebSockets** (which is ran by daphane server), the data is displayed in real-time on the web interface, and it is also stored in the database for future reference. The app supports three stages of tobacco curing: **Initial**, **Mid**, and **Final**, all of which can be customized by the user. 

If the temperature or humidity readings deviate from the user-defined thresholds for any of the curing stages, the app sends notifications via **WhatsApp** to alert the user.

## Features

- **Real-Time Data Display**: The temperature and humidity data from the DHT11 sensor are displayed in real-time on the app interface using WebSockets.
- **Data Storage**: The app stores the captured temperature and humidity data in a database for logging purposes.
- **Stage Configuration**: Users can define temperature and humidity thresholds for each of the curing stages (Initial, Mid, Final).
- **Notifications**: When the temperature or humidity exceeds or drops below the specified limits for the current curing stage, the app sends an automated notification via WhatsApp.
  
## Requirements

- **Python 3.x**
- **Django**
- **Channels** (for WebSockets support)
- **DHT11 Sensor** (hardware component)
- **Twilio API** (for WhatsApp notifications)
- **SQLite** (or other supported databases for data storage)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/tobacco-curing-iot.git
cd tobacco-curing-iot
```

### 2. Create a Virtual Environment

```bash
python3 -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

Run the migrations to set up the database schema:

```bash
python manage.py migrate
```

### 5. Set Up WhatsApp Notifications

To enable WhatsApp notifications, you need a Twilio account. Follow these steps:

1. Create a Twilio account at [twilio.com](https://www.twilio.com/).
2. Set up your **WhatsApp sandbox** for testing.
3. Copy your **Account SID**, **Auth Token**, and **WhatsApp number**.
4. Configure the Twilio settings in the `settings.py` file of the project.

```python
# settings.py
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+1415XXXXXXX'
USER_WHATSAPP_NUMBER = 'whatsapp:+your_user_number'
```

### 6. Run the Development Server

Now you can start the Django development server:

```bash
python manage.py runserver
```

### 7. Access the App

Open a browser and visit:

```
http://127.0.0.1:8000
```

## Usage

- **Configuring Curing Stages**: You can set the temperature and humidity ranges for each stage of the curing process (Initial, Mid, and Final) through the app's web interface.
- **Monitoring Data**: The real-time data from the DHT11 sensor will be displayed on the dashboard.
- **Receiving Notifications**: If the temperature or humidity readings fall outside the defined range for the current curing stage, you will receive a WhatsApp notification.

## WebSockets

The app uses **WebSockets** for real-time data updates. The data from the DHT11 sensor is continuously sent to the front end, allowing you to see the latest temperature and humidity values without needing to refresh the page.

## Database Schema

The app uses a database to store readings of temperature and humidity, along with timestamps. The schema includes the following tables:

- **SensorData**: Stores the real-time readings from the DHT11 sensor.
  - `id`: Auto-incremented ID
  - `temperature`: The current temperature
  - `humidity`: The current humidity
  - `timestamp`: The timestamp of the reading

- **CuringStages**: Stores the stage configuration for the curing process.
  - `id`: Auto-incremented ID
  - `stage_name`: Name of the stage (Initial, Mid, Final)
  - `min_temp`: Minimum temperature threshold for the stage
  - `max_temp`: Maximum temperature threshold for the stage
  - `min_humidity`: Minimum humidity threshold for the stage
  - `max_humidity`: Maximum humidity threshold for the stage

## Contributing

Feel free to contribute to this project. To do so:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to your branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **DHT11 sensor**: For capturing temperature and humidity.
- **Twilio**: For WhatsApp notifications.
- **Django Channels**: For enabling WebSocket functionality.
  
---

Let me know if you need anything adjusted or expanded!
