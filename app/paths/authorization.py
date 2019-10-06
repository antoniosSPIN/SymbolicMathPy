from flask import session, redirect, url_for
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            print('Unauthorized User')
            return redirect(url_for('user.get_login_form'), code=302)
        return f(*args, **kwargs)
    return decorated_function
