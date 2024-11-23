from flask import render_template, jsonify, request
from app import app
from app.database import get_db_connection


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/test', methods=['GET'])
def test_connection():
    connection = get_db_connection()
    if connection:
        return jsonify({"message": "Database connection successful!"}), 200
    return jsonify({"error": "Database connection failed"}), 500


@app.route('/locations', methods=['GET'])
def get_locations():
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM locations;"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(results), 200


@app.route('/add-location', methods=['POST'])
def add_location():
    data = request.json
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = connection.cursor()
    query = """
        INSERT INTO locations (min_latitude, max_latitude, min_longitude, max_longitude, region, country)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    values = (
        data['min_latitude'], data['max_latitude'],
        data['min_longitude'], data['max_longitude'],
        data['region'], data['country']
    )

    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Location added successfully!"}), 201