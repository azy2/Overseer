""" Form with data required to edit a user """
from flask_wtf import FlaskForm
from wtforms import  StringField, HiddenField, ValidationError, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email

from ovs import db
from ovs.models.user_model import User
from ovs.services.user_service import UserService


class ManageUsersForm(FlaskForm):
    """ Form with data required to edit a user """
    user_id = HiddenField('User id', validators=[DataRequired()])
    email = StringField('Email Address', validators=[Email(), DataRequired()])
    first_name = StringField('First Name', validators=[Length(min=1, max=255), DataRequired()])
    last_name = StringField('Last Name', validators=[Length(min=1, max=255), DataRequired()])
    role = SelectField('Role', choices=[('ADMIN', 'Admin'),
                                        ('BUILDING_MANAGER', 'Building Manager'),
                                        ('OFFICE_MANAGER', 'Office Manager'),
                                        ('STAFF', 'Staff'),
                                        ('RESIDENT_ADVISOR', 'Resident Advisor')])
    update_button = SubmitField('Update')
    delete_button = SubmitField('Delete')


    def validate_email(form, field): # pylint: disable=no-self-argument
        """
        Checks whether email is unregistered.

        Args:
            form: The ManageUsersForm that was submitted.
            field: The email field.

        Raises:
            ValidationError: If the email is already in use.
        """
        user = UserService.get_user_by_id(form.user_id.data)
        if user:
            email = user.email
            if (field.data != email) and UserService.get_user_by_email(field.data) is not None:
                raise ValidationError('A user with that email already exists')
        else:
            raise ValidationError('No user with that ID')

    def validate_user_id(form, field):  # pylint: disable=no-self-argument, no-self-use
        """
        Validates that the provided user_id exists.
        This is to thwart malicious input.

        Args:
            form: The ManageUsersForm that was submitted.
            field: The user_id field.

        Raises:
            ValidationError: If the user_id does not exist.
        """
        if db.session.query(User).filter(User.id == field.data).count() == 0:
            raise ValidationError('User does not exist')
