""" Routes under / """
from flask import Blueprint, render_template
from flask_login import current_user

from ovs.services.resident_service import ResidentService
from ovs.services.user_service import UserService
from ovs.utils.roles import UserRole

ovs_bp = Blueprint('/', __name__, )


@ovs_bp.route('/')
def landing_page():
    """ The homepage for OVS """
    kwargs = {}
    if current_user.is_authenticated:
        user = UserService.get_user_by_id(current_user.get_id())
        kwargs['role'] = user.role
        if user.role == UserRole.RESIDENT:
            profile = ResidentService.get_resident_by_id(user.id).profile
            kwargs['profile'] = profile

        else:
            kwargs['user'] = user
    return render_template('index.html', **kwargs)
