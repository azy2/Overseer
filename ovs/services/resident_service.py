"""
DB and utility functions for Residents
"""
import logging
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from ovs import db
from ovs.models.profile_model import Profile
from ovs.models.resident_model import Resident
from ovs.models.user_model import User
from ovs.services.meal_service import MealService
from ovs.services.profile_picture_service import ProfilePictureService
from ovs.utils import genders


class ResidentService:
    """ DB and utility functions for Residents """

    def __init__(self):
        pass

    @staticmethod
    def create_resident(new_user, room_number='None'):
        """
        Adds a resident to the Resident table.

        Args:
            new_user: A User db model.
            room_number: Room number.

        Returns:
            The Resident db model that was just created.
        """
        new_resident = Resident(new_user.id, room_number)
        new_resident_profile = Profile(new_user.id)
        new_resident_profile.preferred_name = new_user.first_name
        new_resident_profile.preferred_email = new_user.email
        new_resident_profile.gender = genders.UNSPECIFIED
        ResidentService.set_default_picture(new_resident_profile.picture_id)

        try:
            db.session.add(new_resident)
            db.session.add(new_resident_profile)
            db.session.commit()
        except SQLAlchemyError:
            # Resident must be unqiue by their email.
            logging.exception('Failed to create resident.')
            db.session.rollback()
            return None

        return new_resident

    @staticmethod
    def edit_resident(user_id, email, first_name, last_name, room_number):
        """
        Edits an existing resident identified by user_id.

        Args:
            user_id: Unique user id.
            email: New email.
            first_name: New first name.
            last_name: New last name.
            room_number: New room number.

        Returns:
            If the edit/update was successful.
        """
        from ovs.services.user_service import UserService
        return (UserService.edit_user(user_id, email, first_name, last_name)
                and ResidentService.update_resident_room_number(user_id, room_number))

    @staticmethod
    def delete_resident(user_id):
        """
        Deletes an existing resident identified by user_id.

        Args:
            user_id: Unique user id.

        Returns:
            If the user was successfuly deleted.
        """
        from ovs.services.profile_service import ProfileService
        resident = ResidentService.get_resident_by_id(user_id)
        if resident is not None:
            if ProfileService.delete_profile(user_id):
                try:
                    db.session.delete(resident)
                    return True
                except SQLAlchemyError:
                    logging.exception('Failed to delete resident.')
                    return False
        return False

    @staticmethod
    def set_default_picture(picture_id):
        """
        TODO: Refactor in to profile_service.
        Sets default picture for new residents.

        Args:
            picture_id: Profile db model picture id.
        """
        default_picture_path = current_app.config['BLOB']['default_picture_path']
        with open(default_picture_path, 'rb') as default_image:
            file_contents = default_image.read()
            file_bytes = bytearray(file_contents)
        ProfilePictureService.create_profile_picture(picture_id, file_bytes)

    @staticmethod
    def get_resident_by_email(email):
        """
        Fetch resident identified by email.

        Args:
            email: A email address.

        Returns:
            A Resident db model.
        """
        try:
            query = db.session.query(Resident)\
                .join(User, User.id == Resident.user_id)
            return query.filter(User.email == email).first()
        except SQLAlchemyError:
            # There should never be multiple user with the same email.
            logging.exception('Failed to get resident by email.')
            return None

    @staticmethod
    def get_resident_by_id(user_id):
        """
        Fetch resident identified by user id.

        Args:
            user_id: Unique user id.

        Returns Resident db model.
        """
        try:
            query = db.session.query(Resident)
            return query.filter_by(user_id=user_id).first()
        except SQLAlchemyError:
            logging.exception('Failed to get resident by id.')
            return None

    @staticmethod
    def resident_exists(user_id):
        """
        Check if resident identified user id exists.

        Args:
            user_id: Unique user id.

        Returns:
            If the residents exists.
        """
        return ResidentService.get_resident_by_id(user_id) is not None

    @staticmethod
    def update_resident_room_number(user_id, room_number):
        """
        Changes the room_number of resident identified by user id.

        Args:
            user_id: Unique user_id that identify a resident.
            room_number: The new room number to assigned to the resident.

        Returns:
            If the update was sucuessful.
        """
        from ovs.services.room_service import RoomService
        if not RoomService.room_exists(room_number):
            return False

        try:
            db.session.query(Resident)\
                .filter(Resident.user_id == user_id)\
                .update({Resident.room_number: room_number})
            db.session.commit()
            return True
        except SQLAlchemyError:
            logging.exception('Failed to update resident room number.')
            db.session.rollback()
            return False

    @staticmethod
    def get_resident_by_pin(pin):
        """
        Fetch resident identified by pin.

        Args:
            pin: Unique meal plan pin.

        Returns:
            A Resident db model.
        """
        try:
            query = db.session.query(Resident)
            return query.filter_by(mealplan_pin=pin).first()
        except SQLAlchemyError:
            logging.exception('Failed to get resient by meal pin.')
            return None

    @staticmethod
    def set_resident_pin(user_id, new_pin):
        """
        Set a meal pin for a resident identified by user id.

        Args:
            user_id: The resident's unique user id.
            new_pin: The new meal pin to be assigned to the resident.

        Returns:
            If the pin was set sucessfully.
        """
        try:
            db.session.query(Resident)\
                .filter_by(user_id=user_id)\
                .update({Resident.mealplan_pin: new_pin})
            db.session.commit()
            return True
        except SQLAlchemyError:
            logging.exception('Failed to set new meal pin for resident.')
            db.session.rollback()
            return False

    @staticmethod
    def create_meal_plan_for_resident_by_email(meal_plan, plan_type, email):
        """
        TODO: Move to meal_service
        Create a new meal plan db entry
          and assign a meal plan pin to an existing resident identified by email.

        Args:
            meal_plan: The plan's maximum credit.
            plan_type: The plan's reset period.
            email: An email address.

        Returns:
            A MealPlan db model.
        """
        resident = ResidentService.get_resident_by_email(email)
        if resident is None:
            return None

        meal_plan = MealService.create_meal_plan(meal_plan, plan_type)
        if meal_plan is None:
            return None

        try:
            resident.mealplan_pin = meal_plan.pin
            db.session.commit()
            return meal_plan
        except SQLAlchemyError:
            logging.exception(
                'Failed to create meal plan for resident identified by email.')
            db.session.rollback()
            return None

        return meal_plan

    @staticmethod
    def get_all_residents_users():
        """
        Fetch all related residents and users in db.

        Returns:
            A list of (Resident, User) db model tuples.
        """
        try:
            return db.session.query(Resident, User).join(User, Resident.user_id == User.id).all()
        except SQLAlchemyError:
            logging.exception('Failed to fetch all residents.')
            return []
