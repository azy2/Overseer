""" Routes under /manager/ """
import datetime
import base64

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from ovs.forms import RegisterRoomForm, RegisterResidentForm, ManageResidentsForm, \
    AddPackageForm, EditPackageForm, MealLoginForm, CreateMealPlanForm, EditMealForm, \
    ManageRoomForm
from ovs.services.meal_service import MealService
from ovs.services.package_service import PackageService
from ovs.services.room_service import RoomService
from ovs.services.user_service import UserService
from ovs.services.resident_service import ResidentService
from ovs.services.profile_picture_service import ProfilePictureService
from ovs.middleware import permissions
from ovs.utils import roles
from ovs.utils import log_types

manager_bp = Blueprint('manager', __name__, )


@manager_bp.route('/', methods=['GET'])
@login_required
@permissions(roles.STAFF)
def landing_page():
    """ The landing page for managers """
    user = UserService.get_user_by_id(current_user.get_id())
    role = user.role
    return render_template('manager/index.html', role=role, user=user)


@manager_bp.route('/manage_rooms/', methods=['GET', 'POST'])
@login_required
@permissions(roles.STAFF)
def manage_rooms():
    """
    /manager/register_room serves an HTML form with input fields for room #,
    status, and type and accepts that form (POST) and adds a room to the
    rooms table. The option for admins to add current residents to said
    room is an available option.
    """
    register_form = RegisterRoomForm()
    rooms = RoomService.get_all_rooms()
    edit_forms = []
    for room in rooms:
        edit_forms.append(ManageRoomForm(prefix=str(room.id)))

    if 'register_btn' in request.form and register_form.validate_on_submit():
        if RoomService.create_room(
                register_form.room_number.data,
                register_form.room_status.data,
                register_form.room_type.data,
                register_form.occupants.data) is None:
            flash('Creating a room failed', 'danger')
        else:
            flash('Successfully created room', 'success')

        return redirect(url_for('manager.manage_rooms'))

    for edit_form in edit_forms:
        if edit_form.delete_button.data:
            if not (RoomService.get_room_by_id(edit_form.room_id.data) and
                    RoomService.delete_room(edit_form.room_id.data)):
                flash('Failed to delete room.', 'danger')
            else:
                flash('Room deleted.', 'success')
            return redirect(url_for('manager.manage_rooms'))
        elif edit_form.update_button.data and edit_form.validate_on_submit():
            if not RoomService.edit_room(
                    edit_form.room_id.data,
                    edit_form.room_number.data,
                    edit_form.status.data,
                    edit_form.room_type.data):
                flash('Falied to update room', 'danger')
            else:
                flash('Room updated!', 'success')
            return redirect(url_for('manager.manage_rooms'))
    user = UserService.get_user_by_id(current_user.get_id())
    role = user.role
    return render_template('manager/manage_rooms.html', role=role, user=user,
                           register_form=register_form, form_data=zip(edit_forms, rooms))


@manager_bp.route('/manage_residents/', methods=['GET', 'POST'])
@login_required
@permissions(roles.STAFF)
def manage_residents():
    """
    /manager/manage_residents serves a HTML with list of residents with their info.
    It allows a manager to add/edit/delete residents with form inputs.
    """
    register_form = RegisterResidentForm(prefix='register_form')
    residents = ResidentService.get_all_residents_users()
    edit_forms = []
    for (_, user) in residents:
        edit_forms.append(ManageResidentsForm(prefix=str(user.id)))

    user = UserService.get_user_by_id(current_user.get_id())
    role = user.role

    if 'register_btn' in request.form and register_form.validate_on_submit():
        if UserService.create_user(
                register_form.email.data,
                register_form.first_name.data,
                register_form.last_name.data,
                "RESIDENT") is None:
            flash('Failed to register resident', 'danger')
        else:
            flash('{} {} registered.'.format(register_form.first_name.data, register_form.last_name.data), 'success')

        return redirect(url_for('manager.manage_residents'))

    for edit_form in edit_forms:
        if edit_form.delete_button.data: #Don't validate. Just delete
            if not (ResidentService.resident_exists(edit_form.user_id.data) and
                    UserService.delete_user(edit_form.user_id.data)):
                flash('Failed to delete resident.', 'danger')
            else:
                flash('Resident deleted.', 'success')

            return redirect(url_for('manager.manage_residents'))

        elif edit_form.update_button.data and edit_form.validate_on_submit():
            room_number = 'None' if edit_form.room_number.data == '' else edit_form.room_number.data
            if not ResidentService.edit_resident(
                    edit_form.user_id.data,
                    edit_form.email.data,
                    edit_form.first_name.data,
                    edit_form.last_name.data,
                    room_number):
                flash('Failed to update resident', 'danger')
            else:
                flash('Resident updated!', 'success')

            return redirect(url_for('manager.manage_residents'))

    return render_template('manager/manage_residents.html', role=role, user=user,
                           register_form=register_form, form_data=zip(edit_forms, residents))


@manager_bp.route('/manage_packages/', methods=['GET', 'POST'])
@login_required
@permissions(roles.STAFF)
def manage_packages():
    """
    /manager/register_resident serves an html form with input fields for email,
    first name, and last name and accepts that form (POST) and adds a user
    to the user table with a default password.
    """
    add_form = AddPackageForm(prefix='add_form')
    packages = PackageService.get_all_packages_recipients()
    edit_forms = []
    for (package, _) in packages:
        edit_forms.append(EditPackageForm(prefix=str(package.id)))

    user = UserService.get_user_by_id(current_user.get_id())
    role = user.role

    if 'add_btn' in request.form and add_form.validate_on_submit():
        recipient_email = add_form.recipient_email.data
        recipient_id = UserService.get_user_by_email(recipient_email).id
        checked_by = '{} {}'.format(user.first_name, user.last_name)
        checked_at = datetime.datetime.now().replace(second=0, microsecond=0)  # Current date/time
        description = add_form.description.data

        PackageService.create_package(recipient_id, checked_by, checked_at, description)
        flash('Package added successfully!', 'success')
        return redirect(url_for('manager.manage_packages'))

    for edit_form in edit_forms:
        if edit_form.complete_button.data:
            if not (PackageService.get_package_by_id(edit_form.package_id.data) and
                    PackageService.delete_package(edit_form.package_id.data)):
                flash('Failed to complete package delivery.', 'danger')
            else:
                flash('Package delivery completed.', 'success')

            return redirect(url_for('manager.manage_packages'))
        if edit_form.update_button.data and edit_form.validate_on_submit():
            PackageService.update_package(edit_form.package_id.data,
                                          edit_form.recipient_email.data,
                                          edit_form.description.data)
            flash('Package edited successfully!', 'success')
            return redirect(url_for('manager.manage_packages'))



    return render_template('manager/manage_packages.html', role=role, user=user,
                           add_form=add_form, form_data=zip(edit_forms, packages))


@manager_bp.route('/meal_login/', methods=['GET', 'POST'])
@login_required
@permissions(roles.STAFF)
def meal_login():
    """
    /manager/meal_login serves an html form with input field pin
    and accepts that form (POST) and logs the use to a meal plan
    """
    form = MealLoginForm()
    user_id = current_user.get_id()
    user = UserService.get_user_by_id(user_id)
    role = user.role


    if form.validate_on_submit():
        mealplan = MealService.get_meal_plan_by_pin(form.pin.data)
        if not MealService.use_meal(form.pin.data, user_id):
            flash('Failed to sign in. Out of meals.', 'danger')

        return redirect(url_for('manager.meal_login'))

    skip = False
    for i, log in enumerate(MealService.get_logs()):
        if skip:
            skip = False
            continue

        if log.log_type == 'UNDO':
            skip = True
            continue

        resident = ResidentService.get_resident_by_id(log.resident_id)
        if resident is None:
            continue
        profile = resident.profile
        pict = base64.b64encode(ProfilePictureService.get_profile_picture(profile.picture_id)).decode()
        mealplan = MealService.get_meal_plan_by_pin(log.mealplan_pin)
        if mealplan is None:
            continue
        current_meals = mealplan.credits
        max_meals = mealplan.meal_plan
        return render_template('manager/meal_login.html', role=role, user=user, form=form,
                               pict=pict, show_undo=(i == 0),
                               name=profile.preferred_name,
                               current_meals=current_meals,
                               max_meals=max_meals)

    return render_template('manager/meal_login.html', role=role, user=user, form=form, no_login=True)

@manager_bp.route('/meal_undo/', methods=['POST'])
@login_required
@permissions(roles.STAFF)
def meal_undo():
    """
    /manager/meal_undo accepts that form (POST) and undo the use of a meal plan
    Currently uses manager id to distinguish frontends. Should use session token.
    """
    user_id = current_user.get_id()

    if request.method == 'POST':
        meal_log = MealService.get_last_log(user_id)

        if meal_log is None or meal_log.log_type == log_types.UNDO:
            flash('Undo invalid', 'danger')
            return redirect(url_for('manager.meal_login'))
        success = MealService.undo_meal_use(user_id, meal_log.resident_id, meal_log.mealplan_pin)
        if not success:
            flash('Undo failed', 'danger')

        resident = ResidentService.get_resident_by_id(meal_log.resident_id)
        mealplan = MealService.get_meal_plan_by_pin(meal_log.mealplan_pin)
        name = resident.profile.preferred_name
        current_meals = mealplan.credits

        flash('{} has {} meals left'.format(name, current_meals), 'success')

    return redirect(url_for('manager.meal_login'))


@manager_bp.route('/manage_meal_plans/', methods=['GET', 'POST'])
@login_required
@permissions(roles.STAFF)
def manage_meal_plans():
    """
    /manager/meal_login serves an html form with input field pin
    and accepts that form (POST) and logs the use to a meal plan
    """
    create_form = CreateMealPlanForm()
    edit_forms = []
    meal_plans = MealService.get_all_meal_plans()
    emails = []
    for meal_plan in meal_plans:
        edit_forms.append(EditMealForm(plan_type=meal_plan.plan_type,
                                       prefix=str(meal_plan.pin)))
        resident = ResidentService.get_resident_by_pin(meal_plan.pin)
        user = UserService.get_user_by_id(resident.user_id)
        emails.append(user.email)

    if 'create_btn' in request.form and create_form.validate_on_submit():
        meal_plan = MealService.create_meal_plan_for_resident_by_email(
            create_form.meal_plan.data,
            create_form.plan_type.data,
            create_form.email.data)
        if meal_plan is None:
            flash('Could not create meal plan.', 'danger')
        else:
            flash('Meal plan created with pin {}'.format(meal_plan.pin), 'success')

        return redirect(url_for('manager.manage_meal_plans'))

    for edit_form in edit_forms:
        if edit_form.delete_button.data:
            if not (MealService.get_meal_plan_by_pin(edit_form.pin.data) and
                    MealService.delete_meal_plan(edit_form.pin.data)):
                flash('Failed to delete meal plan.', 'danger')
            else:
                flash('Meal plan deleted.', 'success')
            return redirect(url_for('manager.manage_meal_plans'))
        elif edit_form.update_button.data and edit_form.validate_on_submit():
            if not MealService.edit_meal_plan(
                    edit_form.pin.data,
                    edit_form.credit.data,
                    edit_form.meal_plan.data,
                    edit_form.plan_type.data):
                flash('Falied to update meal plan', 'danger')
            else:
                flash('Meal plan updated!', 'success')
            return redirect(url_for('manager.manage_meal_plans'))
    user = UserService.get_user_by_id(current_user.get_id())
    role = user.role
    return render_template('manager/manage_meal_plans.html', role=role, user=user,
                           create_form=create_form, form_data=zip(edit_forms, meal_plans, emails))
