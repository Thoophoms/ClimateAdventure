from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

# 1. Locations
class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    min_latitude = db.Column(db.Float)
    max_latitude = db.Column(db.Float)
    min_longitude = db.Column(db.Float)
    max_longitude = db.Column(db.Float)
    region = db.Column(db.String(100))
    country = db.Column(db.String(100))


# 2. Monthly Global Temperature
class MonthlyGlobalTemp(db.Model):
    __tablename__ = "monthly_global_temp"
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    celsius = db.Column(db.Float)
    fahrenheit = db.Column(db.Float)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)


# 3. Temp Log
class TempLog(db.Model):
    __tablename__ = "temp_log"
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    processed_at = db.Column(db.DateTime)
    status = db.Column(db.String(50))


# 4. Monthly Weather Patterns
class MonthlyWeatherPattern(db.Model):
    __tablename__ = "monthly_weather_patterns"
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    total_precipitation = db.Column(db.Float)
    average_wind_speed = db.Column(db.Float)
    solar_radiation = db.Column(db.Float)
    humidity = db.Column(db.Float)
    average_humidity = db.Column(db.Float)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    source = db.Column(db.String(100))


# 5. Live Global Temperature
class LiveGlobalTemp(db.Model):
    __tablename__ = "live_global_temp"
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    temperature_celsius = db.Column(db.Float)
    temperature_fahrenheit = db.Column(db.Float)
    day = db.Column(db.Integer)
    day_of_week = db.Column(db.String(10))
    time = db.Column(db.Time)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)


# 6. Live Weather Patterns
class LiveWeatherPattern(db.Model):
    __tablename__ = "live weather patterns"
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    day = db.Column(db.Date)
    time = db.Column(db.Time)
    total_precipitation = db.Column(db.Float)
    average_wind_speed = db.Column(db.Float)
    solar_radiation = db.Column(db.Float)
    average_humidity = db.Column(db.Float)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    source = db.Column(db.String(100))


# 7. Weather Pattern Log
class WeatherPatternLog(db.Model):
    __tablename__ = "weather_pattern_log"
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    recorded_at = db.Column(db.DateTime)
    processed_at = db.Column(db.DateTime)
    status = db.Column(db.String(50))


# 8. Weather Import Log
class WeatherImportLog(db.Model):
    __tablename__ = "weather_import_log"
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    last_updated = db.Column(db.DateTime)


# 2. Seas
class Sea(db.Model):
    __tablename__ = "seas"
    id = db.Column(db.Integer, primary_key=True)
    sea_name = db.Column(db.String(100))
    min_latitude = db.Column(db.Float)
    max_latitude = db.Column(db.Float)
    min_longitude = db.Column(db.Float)
    max_longitude = db.Column(db.Float)


# 3. Monthly Sea Levels
class MonthlySeaLevel(db.Model):
    __tablename__ = "monthly_sea_levels"
    id = db.Column(db.Integer, primary_key=True)
    sea_id = db.Column(db.Integer, db.ForeignKey("seas.id"))
    average_sea_level = db.Column(db.Float)
    min_sea_level = db.Column(db.Float)
    max_sea_level = db.Column(db.Float)
    anomaly = db.Column(db.Float)
    sea_surface_temperature = db.Column(db.Float)
    month_year = db.Column(db.Date)
    source = db.Column(db.String(100))

    sea = db.relationship("Sea", backref="monthly_sea_levels")


# 4. Sea Level Log
class SeaLevelLog(db.Model):
    __tablename__ = "sea_level_log"
    id = db.Column(db.Integer, primary_key=True)
    sea_id = db.Column(db.Integer, db.ForeignKey("seas.id"))
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    processed_at = db.Column(db.DateTime)
    status = db.Column(db.String(50))

    sea = db.relationship("Sea", backref="sea_level_logs")