from flask import render_template, request, jsonify
from app import app
from app.database import get_db_connection


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    table = request.form.get('table')
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = connection.cursor(dictionary=True)
    try:
        query = f"SELECT * FROM {table};"
        cursor.execute(query)
        rows = cursor.fetchall()
        return jsonify({'data': rows})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        connection.close()
