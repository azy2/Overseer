""" Routes under /manager/ """
import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from ovs.services.room_service import RoomService
from ovs.services.user_service import UserService
from ovs.services.package_service import PackageService
from ovs.services.manager_service import ManagerService
from ovs.services.meal_service import MealService
from ovs.forms import RegisterRoomForm, RegisterResidentForm, ManageResidentsForm, \
    AddPackageForm, EditPackageForm, MealLoginForm, CreateMealPlanForm
manager_bp = Blueprint('manager', __name__,)

@manager_bp.route('/', methods=['GET'])
@login_required
def landing_page():
    """ The landing page for managers """
    user = UserService.get_user_by_id(current_user.get_id()).first()
    role = user.role
    return render_template('/manager/index.html', role=role, user=user)

@manager_bp.route('/register_room/', methods=['GET', 'POST'])
@login_required
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
            room = RoomService.create_room(
                form.room_number.data,
                form.room_status.data,
                form.room_type.data)
            if room is None:
                flash('Room number already exists! Creation Failed!', 'error')
                return redirect((url_for('manager.register_room')))
            occupants = form.occupants.data
            emails = occupants.split(';')
            number = form.room_number.data
            for email in emails:
                if email == '':
                    continue
                # Todo: Add flash response for bad emails
                RoomService.add_resident_to_room(email, number)
            flash('Residents added to rooms successfully!', 'message')
            return redirect(url_for('manager.register_room'))
        else:
            return str(form.errors)
    else:
        user = UserService.get_user_by_id(current_user.get_id()).first()
        role = user.role
        return render_template('manager/register_room.html', role=role, user=user, form=form)


@manager_bp.route('/register_resident/', methods=['GET', 'POST'])
@login_required
def register_resident():
    """
    /manager/register_resident serves an html form with input fields for email,
    first name, and last name and accepts that form (POST) and adds a user
    to the user table with a default password.
    """
    form = RegisterResidentForm(csrf_enabled=False)
    # pylint: disable=duplicate-code
    user = UserService.get_user_by_id(current_user.get_id()).first()
    role = user.role
    if request.method == 'POST':
        print(form) # <-- added !!!
        if form.validate():
            user = UserService.create_user(
                form.email.data,
                form.first_name.data,
                form.last_name.data,
                "RESIDENT")
            if user:
                flash('Residents successfully registered!', 'message')
            else:
                flash('Residents not successfully registered! Email already exists!', 'error')
            # pylint: enable=duplicate-code
            return redirect(url_for('manager.register_resident'))
        else:
            return render_template('manager/register_resident.html', role=role, user=user, form=form)
    else:
        return render_template('manager/register_resident.html', role=role, user=user, form=form)


@manager_bp.route('/manage_residents/', methods=['GET', 'POST'])
@login_required
def manage_residents():
    """
    /manager/manage_residents severs a HTML with list of residents with their info.
    It will also be a link there to add/edit/delete residents with form inputs.
    """
    form = ManageResidentsForm(csrf_enabled=False)
    user = UserService.get_user_by_id(current_user.get_id()).first()
    role = user.role
    if request.method == 'POST':
        if form.validate():
            resident = ManagerService.update_resident_room_number(form.user_id.data, form.room_number.data)
            if resident:
                flash('Resident room number updated successfully!', 'message')
            else:
                flash('Resident room number does not exist or User ID wrong!', 'error')
            return redirect(url_for('manager.manage_residents'))
        else:
            # Todo: display form validation errors on html form fields
            return str(form.errors)
    else:
        return render_template('manager/manage_residents.html', role=role, user=user,
                               residents=ManagerService.get_all_residents(), form=form)


@manager_bp.route('/manage_packages/', methods=['GET', 'POST'])
@login_required
def manage_packages():
    """
    /manager/register_resident serves an html form with input fields for email,
    first name, and last name and accepts that form (POST) and adds a user
    to the user table with a default password.
    """
    add_form = AddPackageForm(prefix='add_form', csrf_enabled=False)
    edit_form = EditPackageForm(prefix='edit_form', csrf_enabled=False)
    user = UserService.get_user_by_id(current_user.get_id()).first()
    role = user.role
    packages_recipients_checkers = ManagerService.get_all_packages_recipients_checkers()
    if request.method == 'POST':
        # Add package
        if add_form.validate_on_submit():
            recipient_email = add_form.recipient_email.data
            recipient_id = UserService.get_user_by_email(recipient_email).first().id
            checked_by_id = current_user.get_id()
            checked_at = datetime.datetime.now().replace(second=0, microsecond=0) # Current date/time
            description = add_form.description.data

            PackageService.create_package(recipient_id, checked_by_id, checked_at, description)
            flash('Package added successfully!', 'message')
            return redirect(url_for('manager.manage_packages'))

        # Edit package
        elif edit_form.validate_on_submit():
            package_id = edit_form.package_id.data
            recipient_email = edit_form.recipient_email.data
            description = edit_form.description.data

            ManagerService.update_package(package_id, recipient_email, description)
            flash('Package edited successfully!', 'message')
            return redirect(url_for('manager.manage_packages'))

        else:
            if 'add_btn' in request.form:
                return render_template('manager/manage_packages.html', role=role, user=user,
                                       packages_recipients_checkers=packages_recipients_checkers,
                                       add_form=add_form, edit_form=edit_form)
            elif 'edit_btn' in request.form:
                flash(str(edit_form.errors['recipient_email'][0]), 'error')
                return redirect(url_for('manager.manage_packages'))

            # Should not reach here
            else:
                return str(add_form.errors) + "\n-----\n" + str(edit_form.errors)

    else:
        return render_template('manager/manage_packages.html', role=role, user=user,
                               packages_recipients_checkers=packages_recipients_checkers,
                               add_form=add_form, edit_form=edit_form)

@manager_bp.route('/meal_login/', methods=['GET', 'POST'])
@login_required
def meal_login():
    """
    /manager/meal_login serves an html form with input field pin
    and accepts that form (POST) and logs the use to a meal plan
    """
    form = MealLoginForm(csrf_enabled=False)
    if request.method == 'POST':
        if form.validate():
            MealService.use_meal(form.pin.data)
            user_plan = MealService.get_meal_plan_by_pin(form.pin.data)
            if user_plan is None:
                return "Invalid login"
            flash('Meal plan login successfully!', 'message')
            return redirect(url_for('manager.meal_login'))
        else:
            return str(form.errors)
    else:
        user = UserService.get_user_by_id(current_user.get_id()).first()
        role = user.role
        return render_template('manager/meal_login.html', role=role, user=user, form=form)

@manager_bp.route('/create_meal_plan/', methods=['GET', 'POST'])
@login_required
def create_meal_plan():
    """
    /manager/meal_login serves an html form with input field pin
    and accepts that form (POST) and logs the use to a meal plan
    """
    form = CreateMealPlanForm(csrf_enabled=False)
    if request.method == 'POST':
        if form.validate():
            UserService.create_meal_plan_for_user_by_email(
                form.pin.data,
                form.meal_plan.data,
                form.plan_type.data,
                form.email.data)
            valid = MealService.get_meal_plan_by_pin(form.pin.data)
            # Todo: meal service always returns false, not fully implemented yet
            if valid:
                flash('Meal plan created successfully!', 'message')
            else:
                flash('Meal plan not created', 'error')
            return redirect(url_for('manager.create_meal_plan'))
        else:
            return str(form.errors)
    else:
        user = UserService.get_user_by_id(current_user.get_id()).first()
        role = user.role
        return render_template('manager/create_meal_plan.html', role=role, user=user, form=form)
