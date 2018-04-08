""" Routes under /manager/ """
import datetime
import base64

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from ovs.forms import RegisterRoomForm, RegisterResidentForm, ManageResidentsForm, \
    AddPackageForm, EditPackageForm, MealLoginForm, CreateMealPlanForm, AddMealForm
from ovs.services.manager_service import ManagerService
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
    user = UserService.get_user_by_id(current_user.get_id()).first()
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
    if request.method == 'POST':
        if form.validate():
            room = RoomService.create_room(
                form.room_number.data,
                form.room_status.data,
                form.room_type.data,
                form.occupants.data)
            if room is None:
                flash('Room number already exists! Creation Failed!', 'error')
                return redirect((url_for('manager.register_room')))
            flash('Residents added to rooms successfully!', 'message')
            return redirect(url_for('manager.register_room'))
        else:
            flash('Input invalid', 'error')
            return redirect(url_for('manager.register_room'))
    else:
        user = UserService.get_user_by_id(current_user.get_id()).first()
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
    edit_form = ManageResidentsForm(prefix='edit_form')

    user = UserService.get_user_by_id(current_user.get_id()).first()
    role = user.role

    if request.method == 'POST':
        if 'delete_btn' in request.form:
            success = UserService.delete_user(edit_form.user_id.data)
            if success:
                flash('Resident successfully deleted')
            else:
                flash('Something went wrong. Could not find resident to delete')
        elif edit_form.validate_on_submit() and 'edit_btn' in request.form:
            success = ResidentService.edit_resident(
                edit_form.user_id.data,
                edit_form.email.data,
                edit_form.first_name.data,
                edit_form.last_name.data,
                edit_form.room_number.data)
            if success:
                flash('Resident updated successfully!', 'message')
            else:
                flash('Room does not exist or duplicate email detected!', 'error')
        elif register_form.validate_on_submit():
            new_user = UserService.create_user(
                register_form.email.data,
                register_form.first_name.data,
                register_form.last_name.data,
                "RESIDENT")
            if new_user:
                flash('Residents successfully registered!', 'message')
            else:
                flash('Residents not successfully registered! Email already exists!', 'error')
        else:
            flash('Input invalid', 'error')
            return redirect(url_for('manager.manage_residents'))
    else:
        return render_template('manager/manage_residents.html', role=role, user=user,
                               residents=ManagerService.get_all_residents(),
                               register_form=register_form, edit_form=edit_form)


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
    edit_form = EditPackageForm(prefix='edit_form')
    user = UserService.get_user_by_id(current_user.get_id()).first()
    role = user.role
    packages_recipients_checkers = ManagerService.get_all_packages_recipients_checkers()
    if request.method == 'POST':
        # Add package
        if add_form.validate_on_submit():
            recipient_email = add_form.recipient_email.data
            recipient_id = UserService.get_user_by_email(recipient_email).first().id
            checked_by_id = current_user.get_id()
            checked_at = datetime.datetime.now().replace(second=0, microsecond=0)  # Current date/time
            description = add_form.description.data

            PackageService.create_package(recipient_id, checked_by_id, checked_at, description)
            flash('Package added successfully!', 'message')
            return redirect(url_for('manager.manage_packages'))

        # Edit package
        elif edit_form.validate_on_submit():
            PackageService.update_package(edit_form.package_id.data,
                                          edit_form.recipient_email.data,
                                          edit_form.description.data)
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
                flash(str(add_form.errors) + "\n-----\n" + str(edit_form.errors), 'error')
                return redirect(url_for('manager.manage_packages'))

    else:
        return render_template('manager/manage_packages.html', role=role, user=user,
                               packages_recipients_checkers=packages_recipients_checkers,
                               add_form=add_form, edit_form=edit_form)


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
    user = UserService.get_user_by_id(user_id).first()
    role = user.role

    if request.method == 'POST':
        # Valid Form
        if form.validate():
            mealplan = MealService.get_meal_plan_by_pin(form.pin.data)
            success = MealService.use_meal(form.pin.data, user_id)

            resident = ResidentService.get_resident_by_pin(mealplan.pin)
            profile = resident.profile
            pict = base64.b64encode(ProfilePictureService.get_profile_picture(profile.picture_id)).decode()
            name = resident.profile.preferred_name
            current_meals = mealplan.credits
            max_meals = mealplan.meal_plan
            return render_template('manager/meal_login.html', role=role, user=user, form=form,
                                   pict=pict, name=name, current_meals=current_meals, max_meals=max_meals
                                   , success=success)

        # Invalid form
        else:
            return render_template('manager/meal_login.html', role=role, user=user, form=form, name=None)
    else:
        return render_template('manager/meal_login.html', role=role, user=user, form=form, name=None)


@manager_bp.route('/meal_undo', methods=['POST'])
@login_required
@permissions(roles.STAFF)
def meal_undo():
    """
    /manager/meal_undo accepts that form (POST) and undo the use of a meal plan
    Currently uses manager id to distinguish frontends. Should use session token.
    """
    form = MealLoginForm()
    user_id = current_user.get_id()
    user = UserService.get_user_by_id(user_id).first()
    role = user.role

    if request.method == 'POST':
        meal_log = MealService.get_last_log(user_id)

        if meal_log is None or meal_log.log_type == log_types.UNDO:
            flash('Undo invalid', 'error')
            return redirect(url_for('manager.meal_login'))
        success = MealService.undo_meal_use(user_id, meal_log.resident_id, meal_log.mealplan_pin)
        if not success:
            flash('Undo unsuccessfully', 'error')

        resident = ResidentService.get_resident_by_id(meal_log.resident_id).first()
        mealplan = MealService.get_meal_plan_by_pin(meal_log.mealplan_pin)
        profile = resident.profile
        pict = base64.b64encode(ProfilePictureService.get_profile_picture(profile.picture_id)).decode()
        name = resident.profile.preferred_name
        current_meals = mealplan.credits
        max_meals = mealplan.meal_plan

        return render_template('manager/meal_login.html', role=role, user=user, form=form,
                               pict=pict, name=name, current_meals=current_meals, max_meals=max_meals)
    else:
        return redirect(url_for('manager.meal_login'))


@manager_bp.route('/create_meal_plan/', methods=['GET', 'POST'])
@login_required
@permissions(roles.OFFICE_MANAGER)
def create_meal_plan():
    """
    /manager/meal_login serves an html form with input field pin
    and accepts that form (POST) and logs the use to a meal plan
    """
    form = CreateMealPlanForm()
    user_id = current_user.get_id()
    user = UserService.get_user_by_id(user_id).first()
    role = user.role
    if request.method == 'POST':
        if form.validate():
            meal_plan = ResidentService.create_meal_plan_for_resident_by_email(
                form.meal_plan.data,
                form.plan_type.data,
                form.email.data)
            if meal_plan is not None:
                flash('Meal plan created successfully with pin: %d' % (meal_plan.pin), 'message')
            else:
                flash('Meal plan not created', 'error')
            return redirect(url_for('manager.create_meal_plan'))
        else:
            return render_template('manager/create_meal_plan.html', role=role, user=user, form=form)
    else:
        return render_template('manager/create_meal_plan.html', role=role, user=user, form=form)


@manager_bp.route('/add_meals/', methods=['GET', 'POST'])
@login_required
@permissions(roles.OFFICE_MANAGER)
def add_meals():
    """
    /manager/meal_login serves an html form with input field pin
    and accepts that form (POST) and logs the use to a meal plan
    """
    form = AddMealForm()
    user = UserService.get_user_by_id(current_user.get_id()).first()
    role = user.role
    if request.method == 'POST':
        if form.validate():
            valid = MealService.add_meals(
                form.pin.data,
                form.number.data)
            if valid:
                user_meal_plan = MealService.get_meal_plan_by_pin(form.pin.data)
                resident = ResidentService.get_resident_by_pin(user_meal_plan.pin)
                message = ('%s has %d out of %d meals now.' % (resident.profile.preferred_name,
                                                               user_meal_plan.credits,
                                                               user_meal_plan.meal_plan))
                flash('Meals added successfully!' + message, 'message')
            else:
                flash('Invalid pin', 'error')
            return redirect(url_for('manager.add_meals'))
        else:
            return render_template('manager/add_meals.html', role=role, user=user, form=form)
    else:
        return render_template('manager/add_meals.html', role=role, user=user, form=form)
