import requests
import time
from datetime import datetime
from models import db, Location, TemperatureLog, WeatherPatternLog, WeatherImportLog
from config import Config

# API Configuration
API_KEY = "cbe4cad6f18ba9b6c67aa9f323f23891"  # Replace with actual API key
CURRENT_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_WEATHER_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Cleanup old data from tables
def cleanup_old_data():
    today = datetime.now().date()
    print("Cleaning up old data...")

    # Delete old entries from tables
    db.session.query(TemperatureLog).filter(TemperatureLog.processed_at < today).delete()
    db.session.query(WeatherPatternLog).filter(WeatherPatternLog.processed_at < today).delete()
    db.session.query(WeatherImportLog).filter(WeatherImportLog.last_updated < today).delete()

    db.session.commit()
    print("Old data cleaned up successfully.")

# Fetch current weather data
def fetch_current_weather(latitude, longitude):
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": API_KEY,
        "units": "metric",
    }
    response = requests.get(CURRENT_WEATHER_URL, params=params)
    response.raise_for_status()
    return response.json()

# Fetch weather forecast data
def fetch_forecast_weather(latitude, longitude):
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": API_KEY,
        "units": "metric",
    }
    response = requests.get(FORECAST_WEATHER_URL, params=params)
    response.raise_for_status()
    return response.json()

# Update the log for the last processed location
def update_log(location_id):
    log = WeatherImportLog.query.filter_by(location_id=location_id).first()
    if log:
        log.last_updated = datetime.utcnow()
    else:
        log = WeatherImportLog(location_id=location_id, last_updated=datetime.utcnow())
        db.session.add(log)
    db.session.commit()

# Get the last processed location
def get_last_processed_location():
    last_log = WeatherImportLog.query.order_by(WeatherImportLog.last_updated.desc()).first()
    return last_log.location_id if last_log else None

# Insert data into TemperatureLog
def insert_temperature_log(location_id, temperature, processed_at):
    temperature_fahrenheit = (temperature * 9 / 5) + 32
    temp_log = TemperatureLog(
        location_id=location_id,
        year=processed_at.year,
        month=processed_at.month,
        temperature=temperature,
        processed_at=processed_at,
        status="SUCCESS"
    )
    db.session.add(temp_log)
    db.session.commit()

# Insert data into WeatherPatternLog
def insert_weather_pattern_log(location_id, precipitation, wind_speed, humidity, processed_at):
    weather_log = WeatherPatternLog(
        location_id=location_id,
        year=processed_at.year,
        month=processed_at.month,
        recorded_at=processed_at,
        processed_at=processed_at,
        status="SUCCESS"
    )
    db.session.add(weather_log)
    db.session.commit()

# Process weather data for all locations
def process_weather_data():
    print("Starting weather data processing...")

    # Clean up old data
    cleanup_old_data()

    # Fetch all locations
    locations = Location.query.all()
    last_location_id = get_last_processed_location()
    resume_index = next((i for i, loc in enumerate(locations) if loc.id == last_location_id), -1) + 1

    for location in locations[resume_index:]:
        try:
            print(f"Processing weather data for Location ID: {location.id} ({location.latitude}, {location.longitude})")
            current_time = datetime.utcnow()

            # Fetch current weather
            current_data = fetch_current_weather(location.latitude, location.longitude)
            temperature = current_data["main"]["temp"]
            precipitation = current_data.get("rain", {}).get("1h", 0)
            wind_speed = current_data["wind"]["speed"]
            humidity = current_data["main"]["humidity"]

            # Insert data into tables
            insert_temperature_log(location.id, temperature, current_time)
            insert_weather_pattern_log(location.id, precipitation, wind_speed, humidity, current_time)

            # Fetch weather forecast
            forecast_data = fetch_forecast_weather(location.latitude, location.longitude)
            for forecast in forecast_data["list"]:
                forecast_time = datetime.strptime(forecast["dt_txt"], "%Y-%m-%d %H:%M:%S")
                temperature = forecast["main"]["temp"]
                precipitation = forecast.get("rain", {}).get("3h", 0)
                wind_speed = forecast["wind"]["speed"]
                humidity = forecast["main"]["humidity"]

                insert_temperature_log(location.id, temperature, forecast_time)
                insert_weather_pattern_log(location.id, precipitation, wind_speed, humidity, forecast_time)

            # Update log
            update_log(location.id)

            print(f"Successfully processed Location ID: {location.id}")
            time.sleep(1)  # Throttle API requests
        except Exception as e:
            print(f"Error processing Location ID {location.id}: {e}")
            db.session.rollback()

    print("Weather data processing completed.")

# Master function to load weather data
def load_weather_data():
    from app import app
    with app.app_context():
        process_weather_data()

if __name__ == "__main__":
    load_weather_data()
