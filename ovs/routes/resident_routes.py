""" under /user/ """
from flask import Blueprint
from ovs.services.resident_service import ResidentService
residents_bp = Blueprint('resident', __name__,)

@residents_bp.route('/view_profile')
def view_profile():
    return 'stuff'

"""
@users_bp.route('/')
def create_user():
    # Example route that generates a random user
    new_user = UserService.create_user(
        ''.join(random.choice(string.ascii_lowercase) for x in range(5)) + '@gmail.com',
        random.choice(string.ascii_uppercase) + ''.join(random.choice(string.ascii_lowercase) for x in range(6)),
        random.choice(string.ascii_uppercase) + ''.join(random.choice(string.ascii_lowercase) for x in range(6)),
        roles.RESIDENT)
    return new_user.json()
"""
