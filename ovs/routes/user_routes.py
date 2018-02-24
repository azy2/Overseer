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
    random_email = ''.join(random.choice(string.ascii_lowercase)
                           for x in range(5)) + '@gmail.com'
    random_first_name = random.choice(
        string.ascii_uppercase) + ''.join(random.choice(string.ascii_lowercase) for x in range(6))
    random_last_name = random.choice(
        string.ascii_uppercase) + ''.join(random.choice(string.ascii_lowercase) for x in range(6))

    new_user = UserService.create_user(
        random_email, random_first_name, random_last_name, roles.RESIDENT)
    return new_user.json()
