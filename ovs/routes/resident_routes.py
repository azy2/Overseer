""" under /resident """
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from ovs import app
from ovs.services.resident_service import ResidentService
from ovs.services.profile_service import ProfileService
from ovs.forms.edit_resident_profile_form import EditResidentProfileForm

residents_bp = Blueprint('resident', __name__)
db = app.database.instance()

@residents_bp.route('/view_profile')
@login_required
def view_profile():
    """
    Displays the profile for the currently logged in user
    """
    resident_id = current_user.get_id()
    resident_profile = ResidentService.get_resident_by_id(resident_id).first().profile
    if resident_profile is None:
        return 'Could not find profile information for user with id: ' + resident_id

    return resident_profile.json()

@residents_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Allows the user to edit their profile in a wtform
    """
    resident_id = current_user.get_id()
    resident_profile = ResidentService.get_resident_by_id(resident_id).first().profile
    if resident_profile is None:
        return 'Could not find profile information for user with id: ' + resident_id

    form = EditResidentProfileForm(obj=resident_profile, csrf_enabled=False)

    if request.method == 'POST':
        if form.validate():
            # Set profile data in database with non-null values from the form
            ProfileService.update_profile(resident_id,
                                          form.preferred_email.data,
                                          form.preferred_name.data,
                                          form.phone_number.data,
                                          form.race.data,
                                          form.gender.data)
            return redirect(url_for('resident.view_profile'))
        else:
            return str(form.errors)
    else:
        return render_template('resident/edit_resident_profile.html', form=form)
