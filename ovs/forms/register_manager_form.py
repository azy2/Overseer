""" Form with data required to register a manager """
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import Email, Length, DataRequired

from ovs.forms.validators import EmailRegistered


class RegisterManagerForm(FlaskForm):
    """ Form with data required to register a manager """
    email = StringField('Email Address', validators=[Email(), DataRequired(), EmailRegistered(False)])
    first_name = StringField('First Name', validators=[Length(min=1, max=255), DataRequired()])
    last_name = StringField('Last Name', validators=[Length(min=1, max=255), DataRequired()])
    role = SelectField('Role', choices=[('ADMIN', 'Admin'),
                                        ('BUILDING_MANAGER', 'Bulding Manager'),
                                        ('OFFICE_MANAGER', 'Office Manager'),
                                        ('STAFF', 'Staff'),
                                        ('RESIDENT_ADVISOR', 'Resident Advisor')])
