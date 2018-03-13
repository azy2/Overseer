""" under /resident """
from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required

from ovs import app
from ovs.forms.edit_resident_profile_form import EditResidentProfileForm
from ovs.services.profile_service import ProfileService
from ovs.services.resident_service import ResidentService
from ovs.utils.roles import UserRole

residents_bp = Blueprint('resident', __name__)
db = app.database.instance()


@residents_bp.route('/')
@login_required
def landing_page():
    """ The landing page for residents """
    resident_id = current_user.get_id()
    resident = ResidentService.get_resident_by_id(resident_id).first()
    profile = resident.profile
    return render_template('resident/index.html', role=UserRole.RESIDENT, profile=profile)


@residents_bp.route('/profile/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Allows the user to edit their profile in a wtform
    """
    resident_id = current_user.get_id()
    profile = ResidentService.get_resident_by_id(resident_id).first().profile
    if profile is None:
        return 'Could not find profile information for user with id: ' + resident_id

    form = EditResidentProfileForm(obj=profile, csrf_enabled=False)

    if request.method == 'POST':
        if form.validate():
            # Set profile data in database with non-null values from the form
            ProfileService.update_profile(resident_id,
                                          form.preferred_email.data,
                                          form.preferred_name.data,
                                          form.phone_number.data,
                                          form.race.data,
                                          form.gender.data)
            flash('Profile edit successfully!', 'message')
            return redirect(url_for('resident.edit_profile'))
        else:
            return str(form.errors)
    else:
        return render_template('resident/profile.html', role=UserRole.RESIDENT, profile=profile, form=form)
