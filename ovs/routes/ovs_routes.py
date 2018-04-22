"""Routes defined under '/'."""
import logging
import base64
import traceback
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from ovs import db
from ovs.services import ProfilePictureService, ProfileService
from ovs.forms import EditResidentProfileForm, UploadProfilePictureForm

ovs_bp = Blueprint('/', __name__, )


@ovs_bp.route('/')
def landing_page():
    """
    The home page accessed by '/'.

    Methods:
        GET.

    Permissions:
        Accessible to ALL.

    Returns:
         A Flask template.
    """
    try:
        kwargs = {}
        if current_user.is_authenticated:
            kwargs['role'] = current_user.role
            kwargs['profile'] = current_user.profile
            kwargs['user'] = current_user
        return render_template('index.html', **kwargs)
    except: # pylint: disable=bare-except
        db.session.rollback()
        flash('An error was encountered', 'danger')
        logging.exception(traceback.format_exc())
        return redirect(url_for('/.landing_page'))

@ovs_bp.route('profile/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Profile edit page accessed by '/profile'.

    Methods:
        GET, POST.

    Permissions:
        Accessible to all users.

    Returns:
        A Flask template.
    """
    try:
        profile = current_user.profile

        profile_form = EditResidentProfileForm(obj=profile)
        picture_form = UploadProfilePictureForm()

        if 'profile_btn' in request.form and profile_form.validate_on_submit():
            # Set profile data in database with non-null values from the form
            ProfileService.update_profile(current_user.get_id(),
                                          profile_form.preferred_email.data,
                                          profile_form.preferred_name.data,
                                          profile_form.phone_number.data,
                                          profile_form.race.data,
                                          profile_form.gender.data)
            db.session.commit()
            flash('Updated profile successfully', 'success')
            return redirect(url_for('/.edit_profile'))
        elif 'picture_btn' in request.form and picture_form.validate_on_submit():
            picture_data = picture_form.profile_picture.data.read()
            ProfilePictureService.update_profile_picture(profile.user_id, picture_data)
            db.session.commit()
            return redirect(url_for('/.edit_profile'))

        pict = base64.b64encode(ProfilePictureService.get_profile_picture(profile.user_id)).decode()
        return render_template('profile.html', role=current_user.role, profile=profile,
                               pict=pict, profile_form=profile_form, picture_form=picture_form)
    except: # pylint: disable=bare-except
        db.session.rollback()
        flash('An error was encountered', 'danger')
        logging.exception(traceback.format_exc())
        return redirect(url_for('/.edit_profile'))
