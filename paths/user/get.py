from paths.user import user
from paths.user.utils import createFormGetResponse


@user.route('/registration', methods=["GET"])
def get_registration_form():
    return createFormGetResponse(template="user/registration.html", error="")


@user.route('/login', methods=["GET"])
def get_login_form():
    return createFormGetResponse(template="user/login.html", error="")
