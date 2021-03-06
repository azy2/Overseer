"""Routes defined under '/admin'."""
import logging
import traceback

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from ovs import db
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
    Manager management page accessed by '/admin/manage_managers'.

    Methods:
        GET, POST.

    Permissions:
        Accessible to ADMIN or higher level users.

    Returns:
        A Flask template.
    """
    try:
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
            db.session.commit()
            flash('{} successfully registered'.format(user.email), 'success')
            return redirect(url_for('admin.manage_managers'))
        for edit_form in edit_forms:
            if edit_form.delete_button.data:
                if UserService.delete_user(edit_form.user_id.data):
                    db.session.commit()
                    flash('User deleted.', 'success')
                else:
                    flash('Cannot delete the last admin.', 'danger')
                return redirect(url_for('admin.manage_managers'))

            elif edit_form.update_button.data and edit_form.validate_on_submit():
                if UserService.edit_user(
                        edit_form.user_id.data,
                        edit_form.email.data,
                        edit_form.first_name.data,
                        edit_form.last_name.data,
                        edit_form.role.data):
                    db.session.commit()
                    flash('User updated!', 'success')
                else:
                    flash('Cannot remove the last admin.', 'danger')

                if edit_form.role.data != 'ADMIN' and edit_form.user_id.data == current_user.get_id():
                    return redirect(url_for('manager.landing_page')) #User lost access to this page.
                return redirect(url_for('admin.manage_managers'))

        user = UserService.get_user_by_id(current_user.get_id())
        role = user.role
        return render_template('admin/manage_managers.html', role=role, user=user,
                               register_form=register_form, form_data=zip(edit_forms, managers),
                               profile=user.profile)
    except: # pylint: disable=bare-except
        db.session.rollback()
        flash('An error was encountered', 'danger')
        logging.exception(traceback.format_exc())
        return redirect(url_for('admin.manage_managers'))
