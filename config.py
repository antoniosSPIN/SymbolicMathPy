import os

# DB info.
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
DB_NAME = os.getenv('DB_NAME', 'astro')

# DB connection string.
SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{password}@{host}:{port}/{db}'\
    .format(user=DB_USER, password=DB_PASSWORD, host=DB_HOST,
            port=DB_PORT, db=DB_NAME)

SQLALCHEMY_TRACK_MODIFICATIONS = False
