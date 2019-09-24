import enum
from flask import render_template

from app import app

class HTTPErrors(enum.Enum):
    BadRequest = 400
    Unauthorized = 401
    Forbidden = 403
    NotFoundError = 404
    InternalServerError = 500


# @app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(500)
def handle_error_pages(err):
    status_code = str(err.get_response().status_code)
    return render_template('utility/' + status_code + '.html'), 404
