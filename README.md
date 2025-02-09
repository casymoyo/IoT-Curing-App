

# Tobacco Curing IoT App

This is a Django-based IoT application designed to monitor and control the tobacco curing process. The system connects to a **DHT11 sensor** to capture real-time temperature and humidity readings. Using **WebSockets**, the data is displayed in real-time on the web interface, and it is also stored in the database for future reference. The app supports three stages of tobacco curing: **Initial**, **Mid**, and **Final**, all of which can be customized by the user. 

If the temperature or humidity readings deviate from the user-defined thresholds for any of the curing stages, the app sends notifications via **WhatsApp** to alert the user.

## Features

- **Real-Time Data Display**: The temperature and humidity data from the DHT11 sensor are displayed in real-time on the app interface using WebSockets.
- **Data Storage**: The app stores the captured temperature and humidity data in a database for logging purposes.
- **Stage Configuration**: Users can define temperature and humidity thresholds for each stage of the curing process (Initial, Mid, Final).
- **Notifications**: When the temperature or humidity exceeds or drops below the specified limits for the current curing stage, the app sends an automated notification via WhatsApp.
  
## Requirements

- **Python 3.12**
- **Django 5.0**
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

## Database Schema

The app uses a database to store readings of temperature and humidity, along with timestamps, user configurations, and logs for alerts. The schema includes the following tables:

### `Stage`
This table defines the three stages of the tobacco curing process (Initial, Mid, Final).

- `id`: Auto-incremented ID
- `name`: Stage name (choices: Initial, Mid, Final)
- `selected`: Boolean indicating if the stage is currently active.

### `Temperature`
This table stores temperature readings recorded from the DHT11 sensor.

- `id`: Auto-incremented ID
- `value`: The current temperature reading
- `timestamp`: The timestamp of the reading
- `stage`: Foreign key to the `Stage` table indicating which stage the reading is associated with.

### `Humidity`
This table stores humidity readings recorded from the DHT11 sensor.

- `id`: Auto-incremented ID
- `value`: The current humidity reading
- `timestamp`: The timestamp of the reading
- `stage`: Foreign key to the `Stage` table indicating which stage the reading is associated with.

### `Config`
This table stores user-defined configuration settings for each curing stage, including temperature and humidity limits.

- `id`: Auto-incremented ID
- `stage`: Stage name (choices: Initial, Mid, Final)
- `name`: The configuration parameter (Temperature or Humidity)
- `lower_limit_value`: The lower limit for the configuration (temperature or humidity)
- `upper_limit_value`: The upper limit for the configuration (temperature or humidity)
- `user`: Foreign key to the `User` table, indicating the user who created the configuration.

### `AlertLog`
This table stores logs of any alerts triggered by deviations in temperature or humidity from the user-defined configurations.

- `id`: Auto-incremented ID
- `timestamp`: The time when the alert was triggered
- `description`: A description of the alert
- `alert_type`: Type of alert (Low, Mid, or High)
- `stage`: Foreign key to the `Stage` table indicating which stage the alert corresponds to.

## WebSockets

The app uses **WebSockets** for real-time data updates. The data from the DHT11 sensor is continuously sent to the front end, allowing you to see the latest temperature and humidity values without needing to refresh the page.

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

Feel free to adjust it further as needed! Let me know if there’s anything else you want to include.
