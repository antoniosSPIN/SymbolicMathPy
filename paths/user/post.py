from flask import render_template, request
from paths.user import user
from paths.user.utils import createFormGetResponse
from models import AuthUser, HasUserRole, UserRole

from app import db


@user.route('/registration', methods=["POST"])
def register_user():
    error = ''
    if request.form['token'] != request.cookies.get('token'):
        error = 'Malformed Request. Please try again!'
        return createFormGetResponse(template="user/registration.html", error=error)
    new_user = AuthUser(request.form['first_name'], request.form['last_name'], request.form['email'], request.form['password'])
    db.session.add(new_user)
    student_role = UserRole.query.filter_by(name="STUDENT").first()
    new_has_user_role = HasUserRole(new_user.auth_user_id, student_role.user_role_id)
    db.session.add(new_has_user_role)
    db.session.commit()
    return render_template("user/registration-successful.html")


@user.route('/login', methods=["POST"])
def login_user():
    error = ''
    if request.form['token'] != request.cookies.get('token'):
        error = 'Malformed Request. Please try again!'
    user = AuthUser.query.filter_by(email=request.form['email'], password=request.form['password']).first()
    if error == '' and not user:
        error = 'The email or the password was incorrect'
    
    if error != '':
        return createFormGetResponse(template="user/login.html", error=error)
    return render_template('user/registration-successful.html')
