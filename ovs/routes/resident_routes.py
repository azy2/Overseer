""" under /resident """
import base64

from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required

from ovs.forms.edit_resident_profile_form import EditResidentProfileForm
from ovs.forms.upload_profile_picture_form import UploadProfilePictureForm
from ovs.services.profile_service import ProfileService
from ovs.services.resident_service import ResidentService
from ovs.services.profile_picture_service import ProfilePictureService
from ovs.middleware import permissions
from ovs.utils import roles

residents_bp = Blueprint('resident', __name__)


@residents_bp.route('/')
@login_required
@permissions(roles.RESIDENT)
def landing_page():
    """ The landing page for residents """
    resident_id = current_user.get_id()
    resident = ResidentService.get_resident_by_id(resident_id).first()
    profile = resident.profile
    return render_template('resident/index.html', role=roles.RESIDENT, profile=profile)


@residents_bp.route('/profile/', methods=['GET', 'POST'])
@login_required
@permissions(roles.RESIDENT)
def edit_profile():
    """
    Allows the user to edit their profile in a wtform
    """
    resident_id = current_user.get_id()
    profile = ResidentService.get_resident_by_id(resident_id).first().profile
    if profile is None:
        return 'Could not find profile information for user with id: ' + resident_id

    profile_form = EditResidentProfileForm(obj=profile)
    picture_form = UploadProfilePictureForm()

    if request.method == 'POST':
        if profile_form.validate_on_submit():
            # Set profile data in database with non-null values from the form
            ProfileService.update_profile(resident_id,
                                          profile_form.preferred_email.data,
                                          profile_form.preferred_name.data,
                                          profile_form.phone_number.data,
                                          profile_form.race.data,
                                          profile_form.gender.data)
        elif picture_form.validate_on_submit():
            picture_data = picture_form.profile_picture.data.read()
            ProfilePictureService.update_profile_picture(profile.picture_id, picture_data)

    pict = base64.b64encode(ProfilePictureService.get_profile_picture(profile.picture_id)).decode()
    print(profile_form.errors)
    print(picture_form.errors)
    return render_template('resident/profile.html', role=roles.RESIDENT, profile=profile, pict=pict,
                           profile_form=profile_form, picture_form=picture_form)
