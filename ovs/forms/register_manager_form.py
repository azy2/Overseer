""" Form with data required to register a manager """
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, ValidationError
from wtforms.validators import Email, Length, DataRequired

from ovs import db
from ovs.services.user_service import UserService


class RegisterManagerForm(FlaskForm):
    """ Form with data required to register a manager """
    email = StringField('Email Address', validators=[Email(), DataRequired()])
    first_name = StringField('First Name', validators=[Length(min=1, max=255), DataRequired()])
    last_name = StringField('Last Name', validators=[Length(min=1, max=255), DataRequired()])
    role = SelectField('Role', choices=[('ADMIN', 'Admin'),
                                        ('BUILDING_MANAGER', 'Bulding Manager'),
                                        ('OFFICE_MANAGER', 'Office Manager'),
                                        ('STAFF', 'Staff'),
                                        ('RESIDENT_ADVISOR', 'Resident Advisor')])

    def validate_email(form, field):
        if UserService.get_user_by_email(field.data) is not None:
            raise ValidationError('An account with this email already exists')
