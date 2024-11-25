import mysql.connector
from mysql.connector import Error

# Database config
DB_CONFIG = {
    'host': 'mysql-database.cn44kuk2at3z.us-east-2.rds.amazonaws.com',
    'user': 'CSIT515',
    'password': 'CSIT515Section1FA24',
    'database': 'weather data'
}


def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to database: {e}")
        return None
