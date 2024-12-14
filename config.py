from urllib.parse import quote_plus



class Config:
    # DB_USER = "CSIT515"
    # DB_PASSWORD = "CSIT515Section1FA24"
    # DB_HOST = "csit515fa24.cn44kuk2at3z.us-east-2.rds.amazonaws.com"
    # DB_NAME = "weather data"

    # DATABASE_URL = 'mysql+pymysql://CSIT515:CSIT515Section1FA24@csit515fa24.cn44kuk2at3z.us-east-2.rds.amazonaws.com/weather%20data'

    # Строка подключения с backticks
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://CSIT515:CSIT515Section1FA24@csit515fa24.cn44kuk2at3z.us-east-2.rds.amazonaws.com/weather data'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
