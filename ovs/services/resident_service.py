"""
DB and utility functions for Residents
"""
import logging

from sqlalchemy.exc import SQLAlchemyError

from ovs import db
from ovs.services.meal_service import MealService
from ovs.models.profile_model import Profile
from ovs.models.resident_model import Resident
from ovs.models.user_model import User
from ovs.utils import genders


class ResidentService:
    """ DB and utility functions for Residents """

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
        from ovs.services.profile_service import ProfileService
        from ovs.services.room_service import RoomService

        new_resident = Resident(new_user.id)
        new_resident_profile = Profile(new_user.id)
        new_resident_profile.preferred_name = new_user.first_name
        new_resident_profile.preferred_email = new_user.email
        new_resident_profile.gender = genders.UNSPECIFIED
        ProfileService.set_default_picture(new_resident_profile.picture_id)

        room = RoomService.get_room_by_number(room_number)
        if room is None:
            logging.exception('Failed to create resident because of invalid room number')
            return None
        new_resident.room_number = room_number

        try:
            db.session.add(new_resident)
            db.session.add(new_resident_profile)
            db.session.commit()
        except SQLAlchemyError:
            # Resident must be unique by their email.
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
        from ovs.services.room_service import RoomService
        return (UserService.edit_user(user_id, email, first_name, last_name)
                and RoomService.add_resident_to_room(email, room_number))

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
        from ovs.services.package_service import PackageService

        resident = ResidentService.get_resident_by_id(user_id)
        if resident is not None:
            meal_delete = True
            if resident.mealplan_pin != 0:
                meal_delete = MealService.delete_meal_plan(resident.mealplan_pin)
            if ProfileService.delete_profile(user_id) and meal_delete \
               and PackageService.delete_packages_for_user(user_id):
                try:
                    db.session.delete(resident)
                    return True
                except SQLAlchemyError:
                    logging.exception('Failed to delete resident.')
                    return False
        return False

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
