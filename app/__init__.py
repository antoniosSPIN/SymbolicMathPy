from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = app.config["SECRET_KEY"]

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
ma = Marshmallow(app)
# import routes
from app import routes
# import error handling
from app import errors
