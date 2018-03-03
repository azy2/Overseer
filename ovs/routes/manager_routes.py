""" routes under /manager/ """
from flask import Blueprint, render_template, request
from ovs.services.room_service import RoomService
from ovs.services.user_service import UserService
from ovs.services.manager_service import ManagerService
from ovs.services.meal_service import MealService
from ovs.forms import RegisterRoomForm, RegisterResidentForm, ManageResidentsForm, MealLoginForm, CreateMealPlanForm
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


@manager_bp.route('/register_resident', methods=['GET', 'POummy values for testingST'])
def register_resident():
    """
    /manager/register_resident serves an html formget_meal_plan_by_pin(pin) with input fields for email,
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


@manager_bp.route('/meal_login', methods=['GET', 'POST'])
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
            return user_plan.json()
        else:
            return str(form.errors)
    else:
        return render_template('manager/meal_login.html', form=form)

@manager_bp.route('/create_meal_plan', methods=['GET', 'POST'])
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
            return MealService.get_meal_plan_by_pin(form.pin.data).json()
        else:
            return str(form.errors)
    else:
        return render_template('manager/create_meal_plan.html', form=form)
