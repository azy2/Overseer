""" under /resident """
from flask import Blueprint
from flask_login import current_user, login_required
from ovs import app
from ovs.services.resident_service import ResidentService

residents_bp = Blueprint('resident', __name__)
db = app.database.instance()

@residents_bp.route('/view_profile')
@login_required
def view_profile():
    """
    Displays the profile for the currently logged in user
    """
    resident_id = current_user.get_id()
    resident_profile = ResidentService.get_resident_profile_by_id(current_user.get_id())
    if(resident_profile == None):
        return 'Could not find profile information for user with id: ' + resident_id

    return 'User ID: ' + resident_id + ' profile: ' + resident_profile
