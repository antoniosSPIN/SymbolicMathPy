import random
from flask import session, render_template, url_for, redirect

from app.paths.authorization import login_required
from app.paths.user import user


@user.route('/registration', methods=['GET'])
def get_registration_form():
    """
        Get registration form
        Renders: user/registration.html
    """
    token = str(random.getrandbits(128))
    session['token'] = token
    return render_template('user/registration.html', token=token, error="")


@user.route('/login', methods=['GET'])
def get_login_form():
    """
        Get login form
        Renders: user/login.html
    """
    token = str(random.getrandbits(128))
    session['token'] = token
    return render_template('user/login.html', token=token, error="")


@user.route('/', methods=['GET'])
@login_required
def get_user_profile():
    """
        Get user profile
        Renders: user/profile.html
    """
    return render_template('user/profile.html')


@user.route('/logout', methods=['GET'])
@login_required
def logout_user():
    """
        Logout user
        Renders: user/logout.html
    """
    session.pop('user_id')
    return redirect(url_for('user.get_login_form'), code=302)
