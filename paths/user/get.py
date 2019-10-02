from flask import session, render_template, url_for, redirect

from paths.authorization import login_required
from paths.user import user
from paths.user.utils import create_form_get_response


@user.route('/registration', methods=["GET"])
def get_registration_form():
    """
        Get registration form
        Renders: user/registration.html
    """
    return create_form_get_response(template="user/registration.html", path='/user/registration', error="")


@user.route('/login', methods=["GET"])
def get_login_form():
    """
        Get login form
        Renders: user/login.html
    """
    return create_form_get_response(template="user/login.html", path='/user/login', error="")


@user.route('/', methods=["GET"])
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
