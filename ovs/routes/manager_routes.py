""" routes under /manager/ """
from flask import Blueprint, render_template, request
from ovs.services import RoomService, UserService
from ovs.forms import RegisterRoomForm, RegisterResidentForm
manager_bp = Blueprint('manager', __name__,)


@manager_bp.route('/register_room', methods=['GET', 'POST'])
def register_room():
    """
    /manager/register_room serves an HTML form with input fields for room #,
    status, and type and accepts that form (POST) and adds a room to the
    rooms table. The option for admins to add current residents to said
    room is an available option.
    """
    form = RegisterRoomForm(csrf_enabled=False)
    if request.method == 'POST':
        if form.validate():
            new_room = RoomService.create_room(
                form.room_number.data,
                form.room_status.data,
                form.room_type.data
            )
            occupants = form.occupants.data
            emails = occupants.split(';')
            number = form.room_number.data
            for email in emails:
                if email == '':
                    continue
                RoomService.add_resident_to_room(email, number)

            return new_room.json()
        else:
            return str(form.errors)
    else:
        return render_template('manager/register_room.html', form=form)


@manager_bp.route('/register_resident', methods=['GET', 'POST'])
def register_resident():
    """
    /manager/register_resident serves an html form with input fields for email,
    first name, and last name and accepts that form (POST) and adds a user
    to the user table with a default password.
    """
    form = RegisterResidentForm(csrf_enabled=False)
    # pylint: disable=duplicate-code
    if request.method == 'POST':
        if form.validate():
            new_user = UserService.create_user(
                form.email.data,
                form.first_name.data,
                form.last_name.data,
                "RESIDENT")
            # pylint: enable=duplicate-code
            return new_user.json()
        else:
            return str(form.errors)
    else:
        return render_template('manager/register_resident.html', form=form)
