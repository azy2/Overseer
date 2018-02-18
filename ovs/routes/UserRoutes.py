from flask import Blueprint
from ovs.services import UserService
from ovs.utils import roles
import random, string
users_bp = Blueprint('user', __name__,)

# TODO delete example route and replace it with real code
@users_bp.route('/')
def create_user():
    new_user = UserService.create_user(''.join(random.choice(string.ascii_lowercase) for x in range(5)) + '@gmail.com',
                                       random.choice(string.ascii_uppercase) + ''.join(random.choice(string.ascii_lowercase) for x in range(6)),
                                       random.choice(string.ascii_uppercase) + ''.join(random.choice(string.ascii_lowercase) for x in range(6)),
                                       roles.RESIDENT)
    return new_user.json()
