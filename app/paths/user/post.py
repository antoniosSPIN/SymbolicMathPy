from flask import render_template, request, session, redirect, url_for

from app.paths.user import user
from app.paths.user.utils import create_form_get_response
from app.models import AuthUser, HasUserRole, UserRole
from app import db


@user.route('/registration', methods=['POST'])
def register_user():
    """
        Register user
        Renders: user/registration-successful.html
        Throws:
            - Malformed request error form.token is not the same as cookies.token
    """
    error = ''
    if request.form['token'] != request.cookies.get('token'):
        error = 'Malformed Request. Please try again!'
        return create_form_get_response(template='user/registration.html', path='/user/registration', error=error)
    new_user = AuthUser(request.form['first_name'], request.form['last_name'], request.form['email'], request.form['password'])
    db.session.add(new_user)
    student_role = UserRole.query.filter_by(name='STUDENT').first()
    new_has_user_role = HasUserRole(new_user.auth_user_id, student_role.user_role_id)
    db.session.add(new_has_user_role)
    db.session.commit()
    return render_template('user/registration-successful.html')


@user.route('/login', methods=['POST'])
def login_user():
    """
        Register user
        Renders: user/registration-successful.html
        Throws:
            - Malformed request error form.token is not the same as cookies.token
            - Authentication error email & password does not match up to any user in database
        Redirects: user.get_user_profile, 302
    """
    error = ''
    if request.form['token'] != request.cookies.get('token'):
        error = 'Malformed Request. Please try again!'
    user = AuthUser.query.filter_by(email=request.form['email'], password=request.form['password']).first()
    if error == '' and not user:
        error = 'The email or the password was incorrect'

    if error != '':
        return create_form_get_response(template="user/login.html", path='/user/login', error=error)
    
    session['user_id'] = user.auth_user_id
    return redirect(url_for('user.get_user_profile'))
