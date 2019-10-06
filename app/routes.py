from app import app
from app.paths.user import user
from app.paths.test import test

# User routes
app.register_blueprint(user, url_prefix='/user')
# Test routes
app.register_blueprint(test, url_prefix='/test')
