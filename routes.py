from app import app
from paths.user import user
from paths.test import test

print("hello")
# User routes
app.register_blueprint(user, url_prefix='/user')
# Test routes
app.register_blueprint(test, url_prefix='/test')
