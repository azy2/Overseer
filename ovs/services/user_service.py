""" DB and utility functions for Users """
from flask import url_for

from ovs import db
from ovs.mail import templates
from ovs.models.user_model import User
from ovs.services.mail_service import MailService
from ovs.services.resident_service import ResidentService
from ovs.services.manager_service import ManagerService
from ovs.services.profile_picture_service import ProfilePictureService
from ovs.utils import crypto, serializer
from ovs.models.profile_model import Profile
from ovs.utils import genders


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
        send_email = False
        if password is None:
            password = crypto.generate_password()
            send_email = True
        new_user = User(email, first_name, last_name, password, role)
        db.session.add(new_user)
        db.session.flush()

        if role == 'RESIDENT':
            ResidentService.create_resident(new_user)

        new_resident_profile = Profile(new_user.id)
        new_resident_profile.preferred_name = new_user.first_name
        new_resident_profile.preferred_email = new_user.email
        new_resident_profile.gender = genders.UNSPECIFIED
        ProfilePictureService.set_default_picture(new_user.id)
        db.session.add(new_resident_profile)
        db.session.flush()

        #Only time passwords are supplied are on default user creation which
        #for which reset password emails are not necessary
        if send_email:
            UserService.send_setup_email(email, first_name, last_name, role)
        return new_user

    @staticmethod
    def edit_user(user_id, email, first_name, last_name, role=None):
        """
        Edits user identified by user id.

        Args:
            user_id: Unique user id.
            email: The user's email.
            first_name: The user's first_name.
            last_name: The user's last_name.
            role: The user's role, or None if it should not change.

        Raises:
            ValueError: If email is already registered.

        Returns:
            bool: True if the user was successfully updated.
                  False if trying to change the role of the last admin
        """
        user = UserService.get_user_by_id(user_id)
        email_user = UserService.get_user_by_email(email)
        # Make user email is not associated with other existing users.
        if email_user is None or email_user == user:
            user.update(email, first_name, last_name)
            db.session.flush()
            db.session.refresh(user)
        else:
            raise ValueError("Email already exists")
        if role:
            if user.role == 'ADMIN' and ManagerService.get_admin_count() == 1:
                return False
            user.role = role
        return True

    @staticmethod
    def delete_user(user_id):
        """
        Deletes an existing user identified by user id.

        Args:
            user_id: Unique user id.

        Returns:
            bool: True if the user was successfuly deleted.
                  False if user_id refers to the last admin.
        """
        user = UserService.get_user_by_id(user_id)
        if user.role == 'ADMIN': # We don't want to delete the last admin
            if ManagerService.get_admin_count() <= 1:
                return False

        delete_picture = user.role == 'RESIDENT'

        db.session.delete(user)
        db.session.flush()

        if delete_picture:
            ProfilePictureService.delete_profile_picture(user_id)

        return True

    @staticmethod
    def send_setup_email(email, first_name, last_name, role):
        """
        Sends a setup email to the email address associated with a user.

        Args:
            email: The user's email address.
            first_name: The user's first name.
            last_name: The user's last name.
            role: The user's role.
        """
        token = serializer.serialize_attr(email, 'ovs-reset-email')
        user_info_substitution = {
            "first_name": first_name,
            "last_name": last_name,
            "role": role.lower(),
            "confirm_url": url_for('auth.reset_user', token=token, _external=True)
        }
        MailService.send_email(email, 'User Account Creation',
                               templates['user_creation_email'],
                               substitutions=user_info_substitution)

    @staticmethod
    def send_reset_email(email):
        """
        Sends a password reset email to the email address associated with a user.

        Args:
            email: The user's email address.
        """
        token = serializer.serialize_attr(email, 'ovs-reset-email')
        user_info_substitution = {
            "reset_url": url_for('auth.reset_user', token=token, _external=True)
        }
        MailService.send_email(email, 'Reset Your Overseer Password',
                               templates['user_reset_email'],
                               substitutions=user_info_substitution)

    @staticmethod
    def get_user_by_email(email):
        """
        Fetch a user identified by email.

        Args:
            email: The user's email address.

        Returns:
            A User db model.
        """
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_id(user_id):
        """
        Fetch a user identified by user id.

        Args:
            user_id: Unique user id.

        Returns:
            A User db model.
        """
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def reset_user(reset_user, new_password):
        """
        Reset a given user's password.

        Args:
            reset_user: User model to reset password of.
            new_password: The new password to set for the given user.

        Returns:
            The updated User model.
        """
        reset_user.update_password(new_password)
        return reset_user
