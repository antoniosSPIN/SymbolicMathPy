from flask import render_template, make_response
from paths.user import user
from paths.user.utils import createRegToken


@user.route('/registration', methods=["GET"])
def get_registration_form():
    reg_token = createRegToken()
    res = make_response(render_template("user-registration.html", error="", reg_token=reg_token))
    res.set_cookie('reg_token', reg_token)
    return res


@user.route('/login', methods=["GET"])
def get_login_form():
    login_token = createRegToken()
    res = make_response(render_template("user-login.html", error="", login_token=login_token))
    res.set_cookie('login_token', login_token)
    return res
