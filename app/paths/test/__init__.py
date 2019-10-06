from app.utils import BaseBlueprint

test = BaseBlueprint('test', __name__)

# Import the user routes.
import app.paths.test.post
import app.paths.test.get
