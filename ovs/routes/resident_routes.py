""" under /resident """
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from ovs import app
from ovs.services.resident_service import ResidentService
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

    if request.method == 'POST' and form.validate():
        # Set profile data in database with non-null values from the form
        if form.preferred_email.data:
            resident_profile.preferred_email = form.preferred_email.data
        if form.preferred_name.data:
            resident_profile.preferred_name = form.preferred_name.data
        if form.phone_number.data:
            resident_profile.phone_number = form.phone_number.data
        if form.race.data:
            resident_profile.race = form.race.data
        if form.gender.data:
            resident_profile.gender = form.gender.data

        db.commit()
        return redirect(url_for('resident.view_profile'))

    return render_template('resident/edit_resident_profile.html', form=form)
