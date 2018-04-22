"""Routes defined under '/resident'."""
import logging
import traceback
import base64

from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import current_user, login_required

from ovs import db
from ovs.services.resident_service import ResidentService
from ovs.services.profile_picture_service import ProfilePictureService
from ovs.middleware import permissions
from ovs.utils import roles

residents_bp = Blueprint('resident', __name__)


@residents_bp.route('/')
@login_required
@permissions(roles.RESIDENT)
def landing_page():
    """
    Home page for residents accessed by '/resident'.

    Methods:
        GET.

    Permissions:
        Accessible to RESIDENT or higher level users.

    Returns:
        A Flask template.
    """
    try:
        resident_id = current_user.get_id()
        resident = ResidentService.get_resident_by_id(resident_id)
        if not resident:
            logging.error('Invalid resident_id %s for route /resident', resident_id)
            return redirect(url_for('/.landing_page'))

        profile = current_user.profile
        packages = resident.packages
        meal_plan = resident.meal_plan
        pict = base64.b64encode(ProfilePictureService.get_profile_picture(profile.user_id)).decode()
        return render_template('resident/index.html', role=roles.RESIDENT, profile=profile, pict=pict,
                               packages=packages, mealplan=meal_plan)
    except: # pylint: disable=bare-except
        db.session.rollback()
        flash('An error was encountered', 'danger')
        logging.exception(traceback.format_exc())
        return redirect(url_for('resident.landing_page'))
