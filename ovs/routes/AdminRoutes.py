from flask import Blueprint, render_template, request
from ovs.services import UserService
from ovs.forms import RegisterManagerForm
admin_bp = Blueprint('admin', __name__,)

@admin_bp.route('/register_manager', methods=['GET', 'POST'])
def register_manager():
    """
    /admin/register_manager serves an html form with input fields for email,
    first name, last name, and role and accepts that form (POST) and adds a user
    to the user table with a default password.
    """
    # TODO: turn CSRF on
    form = RegisterManagerForm(csrf_enabled=False)
    if request.method == 'POST':
        if form.validate():
            new_user = UserService.create_user(
                form.email.data,
                form.first_name.data,
                form.last_name.data,
                form.role.data)
            return new_user.json()
        else:
            return str(form.errors)
    else:
        return render_template('admin/register_manager.html', form=form)
