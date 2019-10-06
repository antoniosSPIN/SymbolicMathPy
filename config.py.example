import os

# DB info.
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "astro")
DB_CHARSET = os.getenv("DB_CHARSET", "utf8")
# DB connection string.
SQLALCHEMY_DATABASE_URI = "mysql://{user}:{password}@{host}:{port}/{db}?charset={charset}"\
    .format(user=DB_USER, password=DB_PASSWORD, host=DB_HOST,
            port=DB_PORT, db=DB_NAME, charset=DB_CHARSET)

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "secret"

BASE_URL = "http://localhost:5000/"
