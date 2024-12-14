import os
from tempfile import NamedTemporaryFile
from flask import Blueprint, request, jsonify, send_file
from models import (
    db, Location, MonthlyGlobalTemp, TempLog, MonthlyWeatherPattern, LiveGlobalTemp,
    LiveWeatherPattern, WeatherPatternLog, Sea, MonthlySeaLevel, SeaLevelLog
)
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Create a Blueprint for export functionality
export_bp = Blueprint('export_bp', __name__)

# ------------------ Utility Functions ------------------

def fetch_table_data(table_name, start_date=None, end_date=None):
    """Fetch filtered data from the specified table."""
    tables = {
        "locations": Location,
        "monthly_global_temp": MonthlyGlobalTemp,
        "temp_log": TempLog,
        "monthly_weather_patterns": MonthlyWeatherPattern,
        "live_global_temp": LiveGlobalTemp,
        "live_weather_patterns": LiveWeatherPattern,
        "weather_pattern_log": WeatherPatternLog,
        "seas": Sea,
        "monthly_sea_levels": MonthlySeaLevel,
        "sea_level_log": SeaLevelLog
    }

    if table_name not in tables:
        return None, f"Table '{table_name}' not found"

    model = tables[table_name]
    query = model.query

    # Apply date filters if applicable
    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")

            # Filter columns with date ranges
            if hasattr(model, "processed_at"):
                query = query.filter(model.processed_at.between(start, end))
            elif hasattr(model, "month_year"):
                query = query.filter(model.month_year.between(start, end))
        except ValueError:
            return None, "Invalid date format. Use YYYY-MM-DD for start_date and end_date."

    # Fetch data
    data = query.all()
    result = [
        {column.name: getattr(row, column.name) for column in row.__table__.columns}
        for row in data
    ]
    return result, None

# ------------------ Routes for Export ------------------

# 1. Export to Excel
@export_bp.route('/export/excel/<string:table_name>', methods=['GET'])
def export_to_excel(table_name):
    try:
        # Get optional date filters from query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        data, error = fetch_table_data(table_name, start_date, end_date)
        if error:
            return jsonify({"error": error}), 404

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Export to Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name=table_name.capitalize())

        output.seek(0)

        # Return the Excel file
        return send_file(
            output,
            as_attachment=True,
            download_name=f"{table_name}.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Generate correlation graph and return as image
@export_bp.route('/export/image/<string:table_name>', methods=['GET'])
def export_image(table_name):
    try:
        # Get optional parameters
        x_column = request.args.get('x')  # Column for X-axis
        y_column = request.args.get('y')  # Column for Y-axis
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # Fetch data
        data, error = fetch_table_data(table_name, start_date, end_date)
        if error:
            return jsonify({"error": error}), 404

        # Convert to DataFrame
        df = pd.DataFrame(data)

        if df.empty or x_column not in df.columns or y_column not in df.columns:
            return jsonify({"error": "Invalid columns or no data available"}), 400

        # Generate the graph
        plt.figure(figsize=(8, 6))
        plt.scatter(df[x_column], df[y_column], alpha=0.7, color='blue')
        plt.title(f"Correlation between {x_column} and {y_column}")
        plt.xlabel(x_column.capitalize())
        plt.ylabel(y_column.capitalize())
        plt.grid(True)
        plt.tight_layout()

        # Save the graph to a temporary file
        temp_file = NamedTemporaryFile(delete=False, suffix=".png")
        plt.savefig(temp_file.name)
        plt.close()

        # Return the image file
        return send_file(
            temp_file.name,
            mimetype='image/png',
            as_attachment=False
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

