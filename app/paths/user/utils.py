from flask import render_template, make_response
import random


def create_form_get_response(template, path, error):
    token = str(random.getrandbits(128))
    res = make_response(render_template(template, error=error, token=token))
    res.set_cookie('token', token, path=path)
    return res
