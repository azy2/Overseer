from flask import Blueprint, render_template, request
from ovs.services import UserService
from ovs.forms import RegisterResidentForm
admin_bp = Blueprint('manager', __name__,)

@admin_bp.route('/register_resident', methods=['GET', 'POST'])
def register_resident():
    """
    /manager/register_resident serves an html form with input fields for email,
    first name, and last name and accepts that form (POST) and adds a user
    to the user table with a default password.
    """
    # TODO: turn CSRF on
    form = RegisterResidentForm(csrf_enabled=False)
    if request.method == 'POST':
        if form.validate():
            new_user = UserService.create_user(
                form.email.data,
                form.first_name.data,
                form.last_name.data,
                "RESIDENT")
            return new_user.json()
        else:
            return str(form.errors)
    else:
        return render_template('manager/register_resident.html', form=form)
