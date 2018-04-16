""" DB and utility functions for Users """
import logging

from sqlalchemy.exc import SQLAlchemyError

from ovs import db
from ovs.mail import templates
from ovs.models.user_model import User
from ovs.services.mail_service import MailService
from ovs.services.resident_service import ResidentService
from ovs.services.manager_service import ManagerService
from ovs.utils import crypto


class UserService:
    """ DB and utility functions for Users """

    @staticmethod
    def create_user(email, first_name, last_name, role, password=None):
        """
        Add a user entry to db.

        Args:
            email: The user's email address.
            first_name: The user's first name.
            last_name: The user's last name.
            role: The user's role.
            password: The user's password. If None a random one is generated.

        Returns:
            A User db model.
        """
        if password is None:
            password = crypto.generate_password()
        new_user = User(email, first_name, last_name, password, role)
        try:
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError:
            logging.exception('Failed to create user.')
            db.session.rollback()
            return None

        if role == 'RESIDENT':
            ResidentService.create_resident(new_user)

        UserService.send_setup_email(
            email, first_name, last_name, role, password)
        return new_user

    @staticmethod
    def edit_user(user_id, email, first_name, last_name):
        """
        Edits user identified by user id.

        Args:
            user_id: Unique user id.
            email: The user's email.
            first_name: The user's first_name.
            last_name: The user's last_name.

        Returns:
            If user was updated sucessfuly.
        """
        user = UserService.get_user_by_id(user_id)
        if user is None:
            return False

        email_user = UserService.get_user_by_email(email)
        # Make user email is not associated with other existing users.
        if email_user is None or email_user == user:
            try:
                user.update(email, first_name, last_name)
                db.session.commit()
                return True
            except SQLAlchemyError:
                logging.exception('Failed to edit user.')
                db.session.rollback()
                return False
        return False

    @staticmethod
    def delete_user(user_id):
        """
        Deletes an existing user identified by user id.

        Args:
            user_id: Unique user id.

        Returns if the user was sucessfuly deleted.
        """
        user = UserService.get_user_by_id(user_id)
        if user is None:
            return False
        if user.role == 'RESIDENT':
            if not ResidentService.delete_resident(user_id):
                return False

        if user.role == 'ADMIN': # We don't want to delete the last admin
            if ManagerService.get_admin_count() <= 1:
                return False
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except SQLAlchemyError:
            logging.exception('Failed to delete user.')
            db.session.rollback()
            return False

    @staticmethod
    def send_setup_email(email, first_name, last_name, role, password):
        """
        Sends a setup email to the email address associated with a user.

        Args:
            email: The user's email address.
            first_name: The user's first name.
            last_name: The user's last name.
            role: The user's role.
            password: The user's password.
        """
        user_info_substitution = {
            "first_name": first_name,
            "last_name": last_name,
            "role": role,
            "password": password
        }
        MailService.send_email(email, 'User Account Creation',
                               templates['user_creation_email'],
                               substitutions=user_info_substitution)

    @staticmethod
    def get_user_by_email(email):
        """
        Fetch a user identified by email.

        Args:
            user_id: The user's email address.

        Returns:
            A User db model.
        """
        try:
            return db.session.query(User).filter_by(email=email).first()
        except SQLAlchemyError:
            logging.exception('Failed to get user by email.')

    @staticmethod
    def get_user_by_id(user_id):
        """
        Fetch a user identified by user id.

        Args:
            user_id: Unique user id.

        Returns:
            A User db model.
        """
        try:
            return db.session.query(User).filter_by(id=user_id).first()
        except SQLAlchemyError:
            logging.exception('Failed to get user by id.')
