from flask import Blueprint, render_template, request
from ovs.services import UserService, ManagerService
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

@manager_bp.route('/manage_residents', methods=['GET', 'POST'])
def manage_residents():
    """
    /manager/manage_residents severs a HTML with list of residents with their info.
    It will also be a link there to add/edit/delete residents with form inputs.
    """
    if request.method == 'GET':
        return render_template('manager/manage_residents.html', residents=ManagerService.get_all_residents())
    elif request.method == 'POST':
        user_id = request.form['user_id']
        room_number = request.form['number']
        return ManagerService.update_resident_room_number(user_id, room_number).json()
