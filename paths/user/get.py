from flask import render_template, make_response
from paths.user import user

import random


@user.route('/registration', methods=["GET"])
def get_registration_form():
    reg_token = str(random.getrandbits(128))
    res = make_response(render_template("user-registration.html", error="", reg_token=reg_token))
    res.set_cookie('reg_token', reg_token)
    return res
