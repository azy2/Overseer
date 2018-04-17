""" routes under /admin/ """
import logging
import traceback

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from ovs import db
from ovs.forms import RegisterManagerForm
from ovs.services import UserService
from ovs.middleware import permissions
from ovs.utils import roles

admin_bp = Blueprint('admin', __name__, )


@admin_bp.route('/register_manager/', methods=['GET', 'POST'])
@login_required
@permissions(roles.ADMIN)
def register_manager():
    """
    /admin/register_manager serves an html form with input fields for email,
    first name, last name, and role and accepts that form (POST) and adds a user
    to the user table with a default password.
    """
    # pylint: disable=duplicate-code

    try:
        user = UserService.get_user_by_id(current_user.get_id())
        role = user.role
        form = RegisterManagerForm()
        if form.validate_on_submit():
            user = UserService.create_user(
                form.email.data,
                form.first_name.data,
                form.last_name.data,
                form.role.data)
            if user is None:
                flash('An error was encountered', 'danger')
            else:
                flash('{} successfully registered'.format(user.email), 'success')

            return redirect(url_for('admin.register_manager'))

        return render_template('admin/register_manager.html', role=role, user=user, form=form)
    except: # pylint: disable=bare-except
        db.session.rollback()
        flash('An error was encountered', 'danger')
        logging.exception(traceback.format_exc())
        return redirect(url_for('admin.register_manager'))
