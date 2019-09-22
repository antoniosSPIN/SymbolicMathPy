from utils import BaseBlueprint

user = BaseBlueprint('user', __name__)

# Import the user routes.
import paths.user.get
import paths.user.post
