from paths.test import test


@test.route("/")
def home():
    return "Hello, World!"
