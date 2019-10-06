from app.utils import BaseBlueprint

user = BaseBlueprint('user', __name__)

# Import the user routes.
import app.paths.user.get
import app.paths.user.post
