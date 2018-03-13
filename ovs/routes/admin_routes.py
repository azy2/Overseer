""" routes under /admin/ """
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from ovs.forms import RegisterManagerForm
from ovs.services import UserService

admin_bp = Blueprint('admin', __name__, )


@admin_bp.route('/register_manager/', methods=['GET', 'POST'])
@login_required
def register_manager():
    """
    /admin/register_manager serves an html form with input fields for email,
    first name, last name, and role and accepts that form (POST) and adds a user
    to the user table with a default password.
    """
    # pylint: disable=duplicate-code

    user = UserService.get_user_by_id(current_user.get_id()).first()
    role = user.role
    form = RegisterManagerForm(csrf_enabled=False)
    if request.method == 'POST':
        if form.validate():
            new_user = UserService.create_user(
                form.email.data,
                form.first_name.data,
                form.last_name.data,
                form.role.data)

            if new_user:
                flash('User successfully added!', 'message')
            else:
                flash('User not successfully added! Email already exists!', 'error')
            return redirect(url_for('admin.register_manager'))
        else:
            return render_template('admin/register_manager.html', role=role, user=user, form=form)
    else:
        return render_template('admin/register_manager.html', role=role, user=user, form=form)
