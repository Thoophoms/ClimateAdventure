from flask import Flask, request, jsonify
from models import (
    db, Location, MonthlyGlobalTemp, TempLog, MonthlyWeatherPattern, LiveGlobalTemp,
    LiveWeatherPattern, WeatherPatternLog, WeatherImportLog, Sea, MonthlySeaLevel, SeaLevelLog
)
from config import Config
from export_data import export_bp  # Import the export blueprint

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Register Blueprint for exporting data
app.register_blueprint(export_bp)

# ------------------ API Endpoints ------------------

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Climate Adventure API!"})

# 1. GET /locations
@app.route('/locations', methods=['GET'])
def get_locations():
    try:
        query = Location.query
        region = request.args.get('region')
        country = request.args.get('country')

        if region:
            query = query.filter_by(region=region)
        if country:
            query = query.filter_by(country=country)

        data = query.all()
        result = [
            {
                "id": loc.id,
                "min_latitude": loc.min_latitude,
                "max_latitude": loc.max_latitude,
                "min_longitude": loc.min_longitude,
                "max_longitude": loc.max_longitude,
                "region": loc.region,
                "country": loc.country
            }
            for loc in data
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 2. GET /monthly-global-temperature
@app.route('/monthly-global-temperature', methods=['GET'])
def get_monthly_global_temperature():
    try:
        query = MonthlyGlobalTemp.query
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        location_id = request.args.get('location_id', type=int)

        if year:
            query = query.filter_by(year=year)
        if month:
            query = query.filter_by(month=month)
        if location_id:
            query = query.filter_by(location_id=location_id)

        data = query.all()
        result = [
            {
                "id": d.id,
                "location_id": d.location_id,
                "celsius": d.celsius,
                "fahrenheit": d.fahrenheit,
                "month": d.month,
                "year": d.year
            }
            for d in data
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 3. GET /temp-log
@app.route('/temp-log', methods=['GET'])
def get_temp_log():
    try:
        data = TempLog.query.all()
        result = [
            {
                "id": d.id,
                "location_id": d.location_id,
                "year": d.year,
                "month": d.month,
                "processed_at": d.processed_at,
                "status": d.status
            }
            for d in data
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 4. GET /monthly-weather-patterns
@app.route('/monthly-weather-patterns', methods=['GET'])
def get_monthly_weather_patterns():
    try:
        data = MonthlyWeatherPattern.query.all()
        result = [
            {
                "id": d.id,
                "location_id": d.location_id,
                "total_precipitation": d.total_precipitation,
                "average_wind_speed": d.average_wind_speed,
                "solar_radiation": d.solar_radiation,
                "humidity": d.humidity,
                "average_humidity": d.average_humidity,
                "month": d.month,
                "year": d.year,
                "source": d.source
            }
            for d in data
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 5. GET /live-global-temp
@app.route('/live-global-temp', methods=['GET'])
def get_live_global_temp():
    try:
        data = LiveGlobalTemp.query.all()
        result = [
            {
                "id": d.id,
                "location_id": d.location_id,
                "temperature_celsius": d.temperature_celsius,
                "temperature_fahrenheit": d.temperature_fahrenheit,
                "day": d.day,
                "day_of_week": d.day_of_week,
                "time": str(d.time),
                "month": d.month,
                "year": d.year
            }
            for d in data
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 6. GET /live-weather-patterns
@app.route('/live-weather-patterns', methods=['GET'])
def get_live_weather_patterns():
    try:
        data = LiveWeatherPattern.query.all()
        result = [
            {
                "id": d.id,
                "location_id": d.location_id,
                "day": d.day,
                "time": str(d.time),
                "total_precipitation": d.total_precipitation,
                "average_wind_speed": d.average_wind_speed,
                "solar_radiation": d.solar_radiation,
                "average_humidity": d.average_humidity,
                "month": d.month,
                "year": d.year,
                "source": d.source
            }
            for d in data
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 7. GET /weather-pattern-log
@app.route('/weather-pattern-log', methods=['GET'])
def get_weather_pattern_log():
    try:
        data = WeatherPatternLog.query.all()
        result = [
            {
                "id": d.id,
                "location_id": d.location_id,
                "year": d.year,
                "month": d.month,
                "recorded_at": d.recorded_at,
                "processed_at": d.processed_at,
                "status": d.status
            }
            for d in data
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 8. GET /seas
@app.route('/seas', methods=['GET'])
def get_seas():
    try:
        query = Sea.query
        sea_name = request.args.get('sea_name')
        min_latitude = request.args.get('min_latitude', type=float)
        max_latitude = request.args.get('max_latitude', type=float)
        min_longitude = request.args.get('min_longitude', type=float)
        max_longitude = request.args.get('max_longitude', type=float)

        if sea_name:
            query = query.filter_by(sea_name=sea_name)
        if min_latitude:
            query = query.filter(Sea.min_latitude >= min_latitude)
        if max_latitude:
            query = query.filter(Sea.max_latitude <= max_latitude)
        if min_longitude:
            query = query.filter(Sea.min_longitude >= min_longitude)
        if max_longitude:
            query = query.filter(Sea.max_longitude <= max_longitude)

        data = query.all()
        result = [
            {
                "id": d.id,
                "sea_name": d.sea_name,
                "min_latitude": d.min_latitude,
                "max_latitude": d.max_latitude,
                "min_longitude": d.min_longitude,
                "max_longitude": d.max_longitude
            }
            for d in data
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# 9. GET /monthly-sea-levels
@app.route('/monthly-sea-levels', methods=['GET'])
def get_monthly_sea_levels():
    try:
        query = MonthlySeaLevel.query
        sea_id = request.args.get('sea_id', type=int)
        month_year = request.args.get('month_year')
        source = request.args.get('source')

        if sea_id:
            query = query.filter_by(sea_id=sea_id)
        if month_year:
            query = query.filter_by(month_year=month_year)
        if source:
            query = query.filter_by(source=source)

        data = query.all()
        result = [
            {
                "id": d.id,
                "sea_id": d.sea_id,
                "average_sea_level": d.average_sea_level,
                "min_sea_level": d.min_sea_level,
                "max_sea_level": d.max_sea_level,
                "anomaly": d.anomaly,
                "sea_surface_temperature": d.sea_surface_temperature,
                "month_year": d.month_year,
                "source": d.source
            }
            for d in data
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# 10. GET /sea-level-log
@app.route('/sea-level-log', methods=['GET'])
def get_sea_level_log():
    try:
        query = SeaLevelLog.query
        sea_id = request.args.get('sea_id', type=int)
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)

        if sea_id:
            query = query.filter_by(sea_id=sea_id)
        if year:
            query = query.filter_by(year=year)
        if month:
            query = query.filter_by(month=month)

        data = query.all()
        result = [
            {
                "id": d.id,
                "sea_id": d.sea_id,
                "year": d.year,
                "month": d.month,
                "processed_at": d.processed_at,
                "status": d.status
            }
            for d in data
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/available-months', methods=['GET'])
def available_months():
    try:

        location_id = request.args.get('location_id', type=int)

        query = MonthlyGlobalTemp.query

        if location_id:
            query = query.filter_by(location_id=location_id)

        months = query.with_entities(
            MonthlyGlobalTemp.year, MonthlyGlobalTemp.month
        ).distinct().order_by(
            MonthlyGlobalTemp.year, MonthlyGlobalTemp.month
        ).all()

        result = [{"year": y, "month": m} for y, m in months]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error":str(e)}), 500


@app.route('/geojson', methods=['GET'])
def get_geojson():
    try:
        # Get query parameters
        parameter = request.args.get('parameter', type=str)
        month = request.args.get('month', type=int)
        year = request.args.get('year', type=int)
        location_id = request.args.get('location_id', type=int)

        if not parameter or not month or not year:
            return jsonify({"error": "Missing required parameters"}), 400

        # Determine the data source based on the parameter
        if parameter in ["total_precipitation", "average_wind_speed", "humidity"]:
            model = MonthlyWeatherPattern
            data_key = parameter
        elif parameter in ["fahrenheit"]:
            model = MonthlyGlobalTemp
            data_key = parameter
        else:
            return jsonify({"error": "Invalid parameter"}), 400

        # Query the data
        query = db.session.query(
            Location.min_longitude,
            Location.min_latitude,
            model.location_id,
            getattr(model, data_key).label("value")
        ).join(Location, Location.id == model.location_id
        ).filter(model.month == month, model.year == year)

        if location_id:
            query = query.filter(model.location_id == location_id)

        data = query.all()
        if not data:
            return jsonify({"error": "No data found"}), 404

        # Generate GeoJSON
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [item.min_longitude, item.min_latitude],
                    },
                    "properties": {
                        "value": item.value,
                        "location_id": item.location_id
                    },
                }
                for item in data
            ],
        }
        return jsonify(geojson), 200
    except Exception as e:
        return jsonify({"error":str(e)}),500

@app.route('/export', methods=['GET'])
def export_data():
    try:
        export_format = request.args.get('format')
        month = request.args.get('month', type=int)
        year = request.args.get('year', type=int)

        if not export_format or not month or not year:
            return jsonify({"error": "Missing required parameters"}), 400

        # Generate data for export (dummy example)
        data = [
            {"location": "Location A", "value": 23.5},
            {"location": "Location B", "value": 19.2},
        ]

        if export_format == "csv":
            from io import StringIO
            import csv

            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=["location", "value"])
            writer.writeheader()
            writer.writerows(data)
            output.seek(0)

            return Response(
                output,
                mimetype="text/csv",
                headers={
                    "Content-Disposition": f"attachment;filename=exported_data_{month}_{year}.csv"
                },
            )
        elif export_format == "pdf":
            from fpdf import FPDF

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Exported Data for {month}/{year}", ln=True, align="C")
            for row in data:
                pdf.cell(200, 10, txt=f"{row['location']}: {row['value']}", ln=True, align="L")

            response = Response(
                pdf.output(dest="S").encode("latin1"),
                mimetype="application/pdf",
                headers={
                    "Content-Disposition": f"attachment;filename=exported_data_{month}_{year}.pdf"
                },
            )
            return response

        else:
            return jsonify({"error": "Invalid format"}), 400

    except Exception as e:
        return jsonify({"error":str(e)}),500
# ------------------ Run Application ------------------
if __name__ == '__main__':
    # Run Flask app
    app.run(debug=True)
