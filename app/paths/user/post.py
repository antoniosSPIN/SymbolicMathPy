import random
from flask import request, session, redirect, url_for, render_template, g

from app.paths.authorization import validate_payload
from app.paths.user import user
from app.paths.user.utils import hasErrors
from app.paths.user.schemas import LoginSchema
from app.models import AuthUser, HasUserRole, UserRole
from app import db, bcrypt


@user.route('/registration', methods=['POST'])
def register_user():
    """
        Register user
        Renders: user/registration-successful.html
        Throws:
            - Malformed request error form.token is not the same as cookies.token
    """
    error = ''
    if request.form['token'] != session['token']:
        error = 'Malformed Request. Please try again!'
    user = AuthUser.query.filter_by(email=request.form['email']).first()
    if not error and user:
        error = 'Email already exists'
    
    if error:
        token = str(random.getrandbits(128))
        session['token'] = token
        return render_template('user/registration.html', token=token, error=error)
    session.pop('token')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    new_user = AuthUser(request.form['first_name'], request.form['last_name'], request.form['email'], pw_hash)
    db.session.add(new_user)
    student_role = UserRole.query.filter_by(name='STUDENT').first()
    new_has_user_role = HasUserRole(new_user.auth_user_id, student_role.user_role_id)
    db.session.add(new_has_user_role)
    db.session.commit()
    return redirect(url_for('user.get_login_form'))


@user.route('/login', methods=['POST'])
@validate_payload(schema=LoginSchema())
def login_user():
    """
        Register user
        Renders: user/registration-successful.html
        Throws:
            - Malformed request error form.token is not the same as cookies.token
            - Authentication error email & password does not match up to any user in database
        Redirects: user.get_user_profile, 302
    """
    error = {}
    if g.errors:
        for field in g.errors:
            error[field] = g.errors[field]

    if 'token' not in request.form or request.form['token'] != session['token']:
        if 'token' not in error:
            error['token'] = []
        error['token'].append('Malformed Request. Please try again!')
    user = AuthUser.query.filter_by(email=request.form['email']).first()

    if error == '' and not user:
        if 'user' not in error:
            error['user'] = []
        error['user'].append('The user does not exist')
    
    if user and not bcrypt.check_password_hash(user.password, request.form['password']):
        if 'password' not in error:
            error['password'] = []
        error['password'].append('Password is incorrect')
    del error['submit']
    if hasErrors(error):
        token = str(random.getrandbits(128))
        session['token'] = token
        return render_template('user/login.html', token=token, error=error)
    session.pop('token')
    session['user_id'] = user.auth_user_id
    return redirect(url_for('user.get_user_profile'))
