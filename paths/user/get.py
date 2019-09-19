from flask import render_template
from paths.user import user


@user.route('/', methods=["GET"])
def home():
    return render_template("user.html")
