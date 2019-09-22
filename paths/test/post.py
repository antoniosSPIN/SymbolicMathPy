from paths.test import test


@test.route("/", methods=["POST"])
def home():
    return "Hello, World!"
