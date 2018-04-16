""" routes under /admin/ """
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from ovs.forms import RegisterManagerForm, ManageUsersForm
from ovs.services import UserService
from ovs.services.manager_service import ManagerService
from ovs.middleware import permissions
from ovs.utils import roles

admin_bp = Blueprint('admin', __name__, )


@admin_bp.route('/manage_managers/', methods=['GET', 'POST'])
@login_required
@permissions(roles.ADMIN)
def manage_managers():
    """
    /admin/manage_managers serves an html form with input fields for email,
    first name, last name, and role and accepts that form (POST) and adds a user
    to the user table with a default password.
    """

    register_form = RegisterManagerForm()
    managers = ManagerService.get_all_managers()
    edit_forms = []
    for user in managers:
        edit_forms.append(ManageUsersForm(role=user.role, prefix=str(user.id)))

    if 'register_btn' in request.form and register_form.validate_on_submit():
        user = UserService.create_user(
            register_form.email.data,
            register_form.first_name.data,
            register_form.last_name.data,
            register_form.role.data)
        if user is None:
            flash('An error was encountered', 'danger')
        else:
            flash('{} successfully registered'.format(user.email), 'success')
        return redirect(url_for('admin.manage_managers'))
    for edit_form in edit_forms:
        if edit_form.delete_button.data:
            if not (UserService.get_user_by_id(edit_form.user_id.data) and
                    UserService.delete_user(edit_form.user_id.data)):
                flash('Failed to delete user.', 'danger')
            else:
                flash('User deleted.', 'success')
            return redirect(url_for('admin.manage_managers'))
        elif edit_form.update_button.data and edit_form.validate_on_submit():
            if not UserService.edit_user(
                    edit_form.user_id.data,
                    edit_form.email.data,
                    edit_form.first_name.data,
                    edit_form.last_name.data):
                flash('Failed to update user!', 'danger')
            else:
                flash('User updated!', 'success')

            return redirect(url_for('admin.manage_managers'))

    user = UserService.get_user_by_id(current_user.get_id())
    role = user.role
    return render_template('admin/manage_managers.html', role=role, user=user,
                           register_form=register_form, form_data=zip(edit_forms, managers))
