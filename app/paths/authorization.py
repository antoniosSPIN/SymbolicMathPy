from flask import session, redirect, url_for, request, g
from functools import wraps


# Decorator to ensure that only a authenticated user will use the call
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            print('Unauthorized User')
            return redirect(url_for('user.get_login_form'), code=302)
        return f(*args, **kwargs)
    return decorated_function


# Decorator to validate payload
def validate_payload(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            g.errors = schema.validate(request.form)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
