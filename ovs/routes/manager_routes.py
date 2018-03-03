""" Routes under /manager/ """
import datetime
from flask import Blueprint, render_template, request
from ovs.services.room_service import RoomService
from ovs.services.user_service import UserService
from ovs.services.package_service import PackageService
from ovs.services.manager_service import ManagerService
from ovs.forms import RegisterRoomForm, RegisterResidentForm, ManageResidentsForm, AddPackageForm, EditPackageForm
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
        print(form) # <-- added !!!
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

@manager_bp.route('/manage_residents', methods=['GET', 'POST'])
def manage_residents():
    """
    /manager/manage_residents severs a HTML with list of residents with their info.
    It will also be a link there to add/edit/delete residents with form inputs.
    """
    form = ManageResidentsForm(csrf_enabled=False)
    if request.method == 'POST':
        if form.validate():
            return ManagerService.update_resident_room_number(
                form.user_id.data, form.room_number.data).json()
        else:
            return str(form.errors)
    else:
        return render_template('manager/manage_residents.html', residents=ManagerService.get_all_residents(), form=form)

@manager_bp.route('/manage_packages', methods=['GET', 'POST'])
def manage_packages():
    """
    /manager/register_resident serves an html form with input fields for email,
    first name, and last name and accepts that form (POST) and adds a user
    to the user table with a default password.
    """
    add_form = AddPackageForm(prefix='add_form', csrf_enabled=False)
    edit_form = EditPackageForm(prefix='edit_form', csrf_enabled=False)
    if request.method == 'POST':
        # Add package
        if add_form.validate_on_submit():
            recipient_email = add_form.recipient_email.data
            recipient_id = UserService.get_user_by_email(recipient_email).first().id
            checked_by_id = 1 # Current user's user id !!!
            checked_at = datetime.datetime.now().replace(second=0, microsecond=0) # Current date/time
            description = add_form.description.data

            print("ADD FORM")
            print(recipient_email)
            print(recipient_id)
            print(checked_by_id)
            print(checked_at)
            print(description)

            new_package = PackageService.create_package(recipient_id, checked_by_id, checked_at, description)
            return new_package.json()

        # Edit package
        elif edit_form.validate_on_submit():
            package_id = edit_form.package_id.data
            recipient_email = edit_form.recipient_email.data
            old_recipient_id = edit_form.recipient_id.data
            description = edit_form.description.data

            print("EDIT FORM")
            print(request.form)
            print(package_id)
            print(recipient_email)
            print(old_recipient_id)
            print(description)

            updated_package = ManagerService.update_package(package_id, recipient_email, description)
            return updated_package.json()

        else:
            if 'add_btn' in request.form:
                return str(add_form.errors)
            elif 'edit_btn' in request.form:
                return str(edit_form.errors)

            # Should not reach here
            else:
                return str(add_form.errors) + "\n-----\n" + str(edit_form.errors)

    else:
        packages_recipients_checkers = ManagerService.get_all_packages_recipients_checkers()
        return render_template('manager/manage_packages.html',
                                packages_recipients_checkers=packages_recipients_checkers,
                                add_form=add_form, edit_form=edit_form)
