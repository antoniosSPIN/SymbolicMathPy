from flask import session, abort, render_template, url_for, redirect

from errors import HTTPErrors
from paths.user import user
from paths.user.utils import create_form_get_response


@user.route('/registration', methods=["GET"])
def get_registration_form():
    return create_form_get_response(template="user/registration.html", path='/user/registration', error="")


@user.route('/login', methods=["GET"])
def get_login_form():
    return create_form_get_response(template="user/login.html", path='/user/login', error="")


@user.route('/', methods=["GET"])
def get_user_profile():
    if 'user_id' not in session:
        print('Unauthorised user')
        abort(HTTPErrors.Unauthorized.value)
    return render_template('user/profile.html')


@user.route('/logout', methods=['GET'])
def logout_user():
    if 'user_id' in session:
        session.pop('user_id')
    else:
        print('Person tried to logout without logging in first')
        abort(HTTPErrors.BadRequest.value)

    return redirect(url_for('user.get_login_form'), code=302)
