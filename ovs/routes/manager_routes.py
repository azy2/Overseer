""" Routes under /manager/ """
import datetime
import base64

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from ovs.forms import RegisterRoomForm, RegisterResidentForm, ManageResidentsForm, \
    AddPackageForm, EditPackageForm, MealLoginForm, CreateMealPlanForm, AddMealForm
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


@manager_bp.route('/register_room/', methods=['GET', 'POST'])
@login_required
@permissions(roles.OFFICE_MANAGER)
def register_room():
    """
    /manager/register_room serves an HTML form with input fields for room #,
    status, and type and accepts that form (POST) and adds a room to the
    rooms table. The option for admins to add current residents to said
    room is an available option.
    """
    form = RegisterRoomForm()
    if form.validate_on_submit():
        if RoomService.create_room(
                form.room_number.data,
                form.room_status.data,
                form.room_type.data,
                form.occupants.data) is None:
            flash('Creating a room failed', 'danger')
        else:
            flash('Successfully created room', 'success')

        return redirect(url_for('manager.register_room'))

    user = UserService.get_user_by_id(current_user.get_id())
    role = user.role
    return render_template('manager/register_room.html', role=role, user=user, form=form)


@manager_bp.route('/manage_residents/', methods=['GET', 'POST'])
@login_required
@permissions(roles.RESIDENT_ADVISOR)
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
@permissions(roles.RESIDENT_ADVISOR)
def manage_packages():
    """
    /manager/register_resident serves an html form with input fields for email,
    first name, and last name and accepts that form (POST) and adds a user
    to the user table with a default password.
    """
    add_form = AddPackageForm(prefix='add_form')
    packages = PackageService.get_all_packages_recipients_checkers() #(package, recip, checker)
    edit_forms = []
    for (package, _, _) in packages:
        edit_forms.append(EditPackageForm(prefix=str(package.id)))

    user = UserService.get_user_by_id(current_user.get_id())
    role = user.role

    if 'add_btn' in request.form and add_form.validate_on_submit():
        recipient_email = add_form.recipient_email.data
        recipient_id = UserService.get_user_by_email(recipient_email).id
        checked_by_id = current_user.get_id()
        checked_at = datetime.datetime.now().replace(second=0, microsecond=0)  # Current date/time
        description = add_form.description.data

        PackageService.create_package(recipient_id, checked_by_id, checked_at, description)
        flash('Package added successfully!', 'success')
        return redirect(url_for('manager.manage_packages'))

    for edit_form in edit_forms:
        if edit_form.update_button.data and edit_form.validate_on_submit():
            PackageService.update_package(edit_form.package_id.data,
                                          edit_form.recipient_email.data,
                                          edit_form.description.data)
            flash('Package edited successfully!', 'success')
            return redirect(url_for('manager.manage_packages'))
        if edit_form.check_button.data and edit_form.validate_on_submit():
            flash('Check package is unimplemented', 'danger')
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
        profile = resident.profile
        pict = base64.b64encode(ProfilePictureService.get_profile_picture(profile.picture_id)).decode()
        mealplan = MealService.get_meal_plan_by_pin(log.mealplan_pin)
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


@manager_bp.route('/create_meal_plan/', methods=['GET', 'POST'])
@login_required
@permissions(roles.STAFF)
def create_meal_plan():
    """
    /manager/meal_login serves an html form with input field pin
    and accepts that form (POST) and logs the use to a meal plan
    """
    form = CreateMealPlanForm()
    user_id = current_user.get_id()
    user = UserService.get_user_by_id(user_id)
    role = user.role
    if form.validate_on_submit():
        meal_plan = MealService.create_meal_plan_for_resident_by_email(
            form.meal_plan.data,
            form.plan_type.data,
            form.email.data)
        if meal_plan is None:
            flash('Could not create meal plan.', 'danger')
        else:
            flash('Meal plan created with pin {}'.format(meal_plan.pin), 'success')

        return redirect(url_for('manager.create_meal_plan'))

    return render_template('manager/create_meal_plan.html', role=role, user=user, form=form)


@manager_bp.route('/add_meals/', methods=['GET', 'POST'])
@login_required
@permissions(roles.STAFF)
def add_meals():
    """
    /manager/meal_login serves an html form with input field pin
    and accepts that form (POST) and logs the use to a meal plan
    """
    form = AddMealForm()
    user = UserService.get_user_by_id(current_user.get_id())
    role = user.role
    if form.validate_on_submit():
        valid = MealService.add_meals(
            form.pin.data,
            form.number.data)
        if valid:
            user_meal_plan = MealService.get_meal_plan_by_pin(form.pin.data)
            resident = ResidentService.get_resident_by_pin(user_meal_plan.pin)
            flash('{} has {} out of {} meals now.'.format(resident.profile.preferred_name,
                                                          user_meal_plan.credits,
                                                          user_meal_plan.meal_plan), 'success')
        else:
            flash('Invalid pin', 'danger')

        return redirect(url_for('manager.add_meals'))

    return render_template('manager/add_meals.html', role=role, user=user, form=form)
