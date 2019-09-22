import random


def createRegToken():
    return str(random.getrandbits(128))
