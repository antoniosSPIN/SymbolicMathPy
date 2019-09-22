from flask import render_template, request, make_response
from paths.user import user

from paths.user.utils import createRegToken

@user.route('/registration', methods=["POST"])
def register_user():
    error = ''
    for name in request.form:
        print(name)
    if request.form['reg_token'] != request.cookies.get('reg_token'):
        error = 'Malformed Request. Please try again!'
        reg_token = createRegToken()
        res = make_response(render_template("user-registration.html", error=error, reg_token=reg_token))
        res.set_cookie('reg_token', reg_token)
        return res
    return render_template("user-registration-successful.html")
