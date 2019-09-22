from flask import render_template, request, make_response
from paths.user import user
from paths.user.utils import createRegToken
from models import AuthUser, HasUserRole, UserRole

from app import db


@user.route('/registration', methods=["POST"])
def register_user():
    error = ''
    if request.form['reg_token'] != request.cookies.get('reg_token'):
        error = 'Malformed Request. Please try again!'
        reg_token = createRegToken()
        res = make_response(render_template("user-registration.html", error=error, reg_token=reg_token))
        res.set_cookie('reg_token', reg_token)
        return res
    new_user = AuthUser(request.form['first_name'], request.form['last_name'], request.form['email'], request.form['password'])
    db.session.add(new_user)
    student_role = UserRole.query.filter_by(name="STUDENT").first()
    new_has_user_role = HasUserRole(new_user.auth_user_id, student_role.user_role_id)
    db.session.add(new_has_user_role)
    db.session.commit()
    return render_template("user-registration-successful.html")


@user.route('/login', methods=["POST"])
def login_user():
    error = ''
    if request.form['login_token'] != request.cookies.get('login_token'):
        error = 'Malformed Request. Please try again!'
        login_token = createRegToken()
        res = make_response(render_template("user-login.html", error=error, login_token=login_token))
        res.set_cookie('login_token', login_token)
        return res
    user = AuthUser.query.filter_by(email=request.form['email'], password=request.form['password']).first()
    if not user:
        error = 'The email or the password was incorrect'
        login_token = createRegToken()
        res = make_response(render_template("user-login.html", error=error, login_token=login_token))
        res.set_cookie('login_token', login_token)
        return res
    return render_template('user-registration-successful.html')
