""" routes under /user/ """
import random
import string
from flask import Blueprint
from ovs.services import UserService
from ovs.utils import roles
users_bp = Blueprint('user', __name__,)


@users_bp.route('/')
def create_user():
    """ Example route that generates a random user """
    new_user = UserService.create_user(
        ''.join(random.choice(string.ascii_lowercase) for x in range(5)) + '@gmail.com',
        random.choice(string.ascii_uppercase) + ''.join(random.choice(string.ascii_lowercase) for x in range(6)),
        random.choice(string.ascii_uppercase) + ''.join(random.choice(string.ascii_lowercase) for x in range(6)),
        roles.RESIDENT)
    return new_user.json()
