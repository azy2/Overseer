""" routes under /admin/ """
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from ovs.services import UserService
from ovs.forms import RegisterManagerForm
admin_bp = Blueprint('admin', __name__,)


@admin_bp.route('/register_manager/', methods=['GET', 'POST'])
@login_required
def register_manager():
    """
    /admin/register_manager serves an html form with input fields for email,
    first name, last name, and role and accepts that form (POST) and adds a user
    to the user table with a default password.
    """
    form = RegisterManagerForm(csrf_enabled=False)
    # pylint: disable=duplicate-code
    if request.method == 'POST':
        if form.validate():
            UserService.create_user(
                form.email.data,
                form.first_name.data,
                form.last_name.data,
                form.role.data)
            # pylint: enable=duplicate-code
            return redirect(url_for('admin.register_manager'))
        else:
            return str(form.errors)
    else:
        user = UserService.get_user_by_id(current_user.get_id()).first()
        role = user.role
        return render_template('admin/register_manager.html', role=role, user=user, form=form)
