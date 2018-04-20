"""Routes defined under '/resident'."""
import logging
import traceback

from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import current_user, login_required

from ovs import db
from ovs.services.resident_service import ResidentService
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
        return render_template('resident/index.html', role=roles.RESIDENT, profile=profile)
    except: # pylint: disable=bare-except
        db.session.rollback()
        flash('An error was encountered', 'danger')
        logging.exception(traceback.format_exc())
        return redirect(url_for('resident.landing_page'))
