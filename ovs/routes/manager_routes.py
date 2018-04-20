"""Routes defined under '/manager'."""
import datetime
import base64
import logging
import traceback

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required

from ovs import db
from ovs.forms import RegisterRoomForm, RegisterResidentForm, ManageResidentsForm, \
    AddPackageForm, EditPackageForm, MealLoginForm, CreateMealPlanForm, EditMealForm, \
    ManageRoomForm
from ovs.services.meal_service import MealService
from ovs.services.package_service import PackageService
from ovs.services.room_service import RoomService
from ovs.services.user_service import UserService
from ovs.services.resident_service import ResidentService
from ovs.services.profile_picture_service import ProfilePictureService
from ovs.services.manager_service import ManagerService
from ovs.middleware import permissions
from ovs.utils import roles
from ovs.utils import log_types

manager_bp = Blueprint('manager', __name__, )


@manager_bp.route('/', methods=['GET'])
@login_required
@permissions(roles.STAFF)
def landing_page():
    """
    Home page for managers accessed by '/manager'.

    Methods:
        GET.

    Permissions:
        Accessible to STAFF or higher level users.

    Returns:
        A Flask template.
    """
    try:
        user = UserService.get_user_by_id(current_user.get_id())
        role = user.role
        empty_room_nums = ManagerService.get_empty_room_nums()
        num_residents = ManagerService.get_num_residents()
        today_num_packages, total_num_packages = ManagerService.get_package_info()
        aggregate_meal_usage = ManagerService.get_aggregate_meal_usage()
        return render_template('manager/index.html', role=role, user=user, empty_room_nums=empty_room_nums,
                               num_residents=num_residents, total_num_packages=total_num_packages,
                               today_num_packages=today_num_packages, aggregate_meal_usage=aggregate_meal_usage)
    except: # pylint: disable=bare-except
        db.session.rollback()
        flash('An error was encountered', 'danger')
        logging.exception(traceback.format_exc())
        return redirect(url_for('manager'))


@manager_bp.route('/manage_rooms/', methods=['GET', 'POST'])
@login_required
@permissions(roles.STAFF)
def manage_rooms():
    """
    Rooms management page accessed by '/manager/manage_rooms'.

    Methods:
        GET, POST.

    Permissions:
        Accessible to STAFF or higher level users.

    Returns:
        A Flask template.
    """
    try:
        register_form = RegisterRoomForm()
        rooms = RoomService.get_all_rooms()
        edit_forms = []
        for room in rooms:
            edit_forms.append(ManageRoomForm(prefix=str(room.id)))

        if 'register_btn' in request.form and register_form.validate_on_submit():
            RoomService.create_room(
                register_form.room_number.data,
                register_form.room_status.data,
                register_form.room_type.data,
                register_form.occupants.data)
            db.session.commit()
            flash('Successfully created room', 'success')

            return redirect(url_for('manager.manage_rooms'))

        for edit_form in edit_forms:
            if edit_form.delete_button.data:
                RoomService.delete_room(edit_form.room_id.data)
                db.session.commit()
                flash('Room deleted.', 'success')
                return redirect(url_for('manager.manage_rooms'))

            elif edit_form.update_button.data and edit_form.validate_on_submit():
                if RoomService.edit_room(
                        edit_form.room_id.data,
                        edit_form.room_number.data,
                        edit_form.status.data,
                        edit_form.room_type.data):
                    db.session.commit()
                    flash('Room updated!', 'success')
                else:
                    flash('Duplicate room number detected!', 'danger')
                return redirect(url_for('manager.manage_rooms'))

        user = UserService.get_user_by_id(current_user.get_id())
        role = user.role
        return render_template('manager/manage_rooms.html', role=role, user=user,
                               register_form=register_form, form_data=zip(edit_forms, rooms))
    except: # pylint: disable=bare-except
        db.session.rollback()
        flash('An error was encountered', 'danger')
        logging.exception(traceback.format_exc())
        return redirect(url_for('manager.manage_rooms'))


@manager_bp.route('/get_residents/', methods=['POST'])
@login_required
@permissions(roles.STAFF)
def get_residents():
    """
    Get all resident email request accessed by '/manager/get_residents'.

    Methods:
        POST.

    Permissions:
        Accessible to STAFF or higher level users.

    Returns:
        A json object.
    """
    try:
        residents_users = ResidentService.get_all_residents_users()
        emails = []
        for _, user in residents_users:
            emails.append(user.email)
        return jsonify(emails)
    except: # pylint: disable=bare-except
        flash('An error was encountered', 'danger')
        logging.exception(traceback.format_exc())
        return jsonify([])

@manager_bp.route('/manage_residents/', methods=['GET', 'POST'])
@login_required
@permissions(roles.STAFF)
def manage_residents():
    """
    Residents management page accessed by '/manager/manage_residents'.

    Methods:
        GET, POST.

    Permissions:
        Accessible to STAFF or higher level users.

    Returns:
        A Flask template.
    """
    try:
        register_form = RegisterResidentForm(prefix='register_form')
        residents = ResidentService.get_all_residents_users()
        edit_forms = []
        for (_, user) in residents:
            edit_forms.append(ManageResidentsForm(prefix=str(user.id)))

        user = UserService.get_user_by_id(current_user.get_id())
        role = user.role

        if 'register_btn' in request.form and register_form.validate_on_submit():
            UserService.create_user(
                register_form.email.data,
                register_form.first_name.data,
                register_form.last_name.data,
                "RESIDENT")

            db.session.commit()
            flash('{} {} registered.'.format(register_form.first_name.data, register_form.last_name.data), 'success')

            return redirect(url_for('manager.manage_residents'))

        for edit_form in edit_forms:
            if edit_form.delete_button.data:  # Don't validate. Just delete
                UserService.delete_user(edit_form.user_id.data)
                db.session.commit()
                flash('Resident deleted.', 'success')

                return redirect(url_for('manager.manage_residents'))

            elif edit_form.update_button.data and edit_form.validate_on_submit():
                ResidentService.edit_resident(
                    edit_form.user_id.data,
                    edit_form.email.data,
                    edit_form.first_name.data,
                    edit_form.last_name.data,
                    edit_form.room_number.data)
                db.session.commit()
                flash('Resident updated!', 'success')

                return redirect(url_for('manager.manage_residents'))

        return render_template('manager/manage_residents.html', role=role, user=user,
                               register_form=register_form, form_data=zip(edit_forms, residents))
    except: # pylint: disable=bare-except
        db.session.rollback()
        flash('An error was encountered', 'danger')
        logging.exception(traceback.format_exc())
        return redirect(url_for('manager.manage_residents'))


@manager_bp.route('/manage_packages/', methods=['GET', 'POST'])
@login_required
@permissions(roles.STAFF)
def manage_packages():
    """
    Package management page accessed by '/manager/manage_packages'.

    Methods:
        GET, POST.

    Permissions:
        Accessible to STAFF or higher level users.

    Returns:
        A Flask template.
    """
    try:
        add_form = AddPackageForm(prefix='add_form')
        packages_recipients = PackageService.get_all_packages_recipients()
        edit_forms = []
        for (package, _) in packages_recipients:
            edit_forms.append(EditPackageForm(prefix=str(package.id)))

        user = UserService.get_user_by_id(current_user.get_id())
        role = user.role

        if 'check_btn' in request.form and add_form.validate_on_submit():
            recipient_email = add_form.recipient_email.data
            recipient_id = UserService.get_user_by_email(recipient_email).id
            checked_by = '{} {}'.format(user.first_name, user.last_name)
            checked_at = datetime.datetime.now() # Current date/time
            description = add_form.description.data

            PackageService.create_package(recipient_id, checked_by, checked_at, description)

            db.session.commit()
            flash('Package added successfully!', 'success')
            return redirect(url_for('manager.manage_packages'))

        for edit_form in edit_forms:
            if edit_form.deliver_button.data:
                PackageService.delete_package(edit_form.package_id.data)
                db.session.commit()
                flash('Package delivery completed.', 'success')
                return redirect(url_for('manager.manage_packages'))

            elif edit_form.update_button.data and edit_form.validate_on_submit():
                PackageService.update_package(edit_form.package_id.data,
                                              edit_form.recipient_id.data,
                                              edit_form.description.data)
                db.session.commit()
                flash('Package edited successfully!', 'success')
                return redirect(url_for('manager.manage_packages'))

        return render_template('manager/manage_packages.html', role=role, user=user,
                               add_form=add_form, form_data=zip(edit_forms, packages_recipients))
    except: # pylint: disable=bare-except
        db.session.rollback()
        flash('An error was encountered', 'danger')
        logging.exception(traceback.format_exc())
        return redirect(url_for('manager.manage_packages'))


@manager_bp.route('/meal_login/', methods=['GET', 'POST'])
@login_required
@permissions(roles.STAFF)
def meal_login():
    """
    Meal login page accessed by 'manager/meal_login'.

    Methods:
        GET, POST.

    Permissions:
        Accessible to STAFF or higher level users.

    Returns:
        A Flask template.
    """
    try:
        form = MealLoginForm()
        user_id = current_user.get_id()
        user = UserService.get_user_by_id(user_id)
        role = user.role

        if form.validate_on_submit():
            mealplan = MealService.get_meal_plan_by_pin(form.pin.data)
            used = MealService.use_meal(form.pin.data, user_id)
            db.session.commit()
            if not used:
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
            pict = base64.b64encode(ProfilePictureService.get_profile_picture(profile.user_id)).decode()
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
    except: # pylint: disable=bare-except
        db.session.rollback()
        flash('An error was encountered', 'danger')
        logging.exception(traceback.format_exc())
        return redirect(url_for('manager.meal_login'))


@manager_bp.route('/meal_undo/', methods=['POST'])
@login_required
@permissions(roles.STAFF)
def meal_undo():
    """
    Undo meal request accessed by '/manager/meal_undo'.

    Methods:
        POST.

    Permissions:
        Accessible to STAFF or higher level users.

    Returns:
        A Flask template.
    """
    try:
        user_id = current_user.get_id()

        meal_log = MealService.get_last_log(user_id)

        if meal_log is None or meal_log.log_type == log_types.UNDO:
            flash('Undo invalid', 'danger')
            return redirect(url_for('manager.meal_login'))
        MealService.undo_meal_use(user_id, meal_log.resident_id, meal_log.mealplan_pin)

        resident = ResidentService.get_resident_by_id(meal_log.resident_id)
        mealplan = MealService.get_meal_plan_by_pin(meal_log.mealplan_pin)
        name = resident.profile.preferred_name
        current_meals = mealplan.credits

        db.session.commit()
        flash('{} has {} meals left'.format(name, current_meals), 'success')

        return redirect(url_for('manager.meal_login'))
    except: # pylint: disable=bare-except
        db.session.rollback()
        flash('Failed to undo', 'danger')
        logging.exception(traceback.format_exc())
        return redirect(url_for('manager.meal_undo'))


@manager_bp.route('/manage_meal_plans/', methods=['GET', 'POST'])
@login_required
@permissions(roles.STAFF)
def manage_meal_plans():
    """
    Meal plan mangement page accessed by '/manager/manage_meal_plans'.

    Methods:
        GET, POST.

    Permissions:
        Accessible to STAFF or higher level users.

    Returns:
        A Flask template.
    """
    try:
        create_form = CreateMealPlanForm()
        edit_forms = []
        meal_plans = MealService.get_all_meal_plans()
        emails = []
        for meal_plan in meal_plans:
            edit_forms.append(EditMealForm(plan_type=meal_plan.plan_type,
                                           prefix=str(meal_plan.pin)))
            resident = ResidentService.get_resident_by_pin(meal_plan.pin)
            emails.append(resident.user.email)

        if 'create_btn' in request.form and create_form.validate_on_submit():
            meal_plan = MealService.create_meal_plan_for_resident_by_email(
                create_form.meal_plan.data,
                create_form.plan_type.data,
                create_form.email.data)
            db.session.commit()
            flash('Meal plan created with pin {}'.format(meal_plan.pin), 'success')

            return redirect(url_for('manager.manage_meal_plans'))

        for edit_form in edit_forms:
            if edit_form.delete_button.data:
                MealService.delete_meal_plan(edit_form.pin.data)
                db.session.commit()
                flash('Meal plan deleted.', 'success')
                return redirect(url_for('manager.manage_meal_plans'))
            elif edit_form.update_button.data and edit_form.validate_on_submit():
                MealService.edit_meal_plan(
                    edit_form.pin.data,
                    edit_form.credit.data,
                    edit_form.meal_plan.data,
                    edit_form.plan_type.data)
                db.session.commit()
                flash('Meal plan updated!', 'success')
                return redirect(url_for('manager.manage_meal_plans'))

        user = UserService.get_user_by_id(current_user.get_id())
        role = user.role
        return render_template('manager/manage_meal_plans.html', role=role, user=user,
                               create_form=create_form, form_data=zip(edit_forms, meal_plans, emails))
    except: # pylint: disable=bare-except
        db.session.rollback()
        flash('An error was encountered', 'danger')
        logging.exception(traceback.format_exc())
        return redirect(url_for('manager.create_meal_plan'))
