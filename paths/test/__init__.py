from utils import BaseBlueprint

test = BaseBlueprint('test', __name__)

# Import the user routes.
import paths.test.post
