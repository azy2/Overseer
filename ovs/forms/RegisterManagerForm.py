from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import Length, DataRequired

class RegisterManagerForm(FlaskForm):
    email = StringField('Email Address', validators = [Length(min=6, max=35), DataRequired()])
    first_name = StringField('First Name', validators = [Length(min=1, max=255), DataRequired()])
    last_name = StringField('Last Name', validators = [Length(min=1, max=255), DataRequired()])
    role = SelectField('Role', choices=[('ADMIN', 'Admin'),
                                        ('BUILDING_MANAGER', 'Bulding Manager'),
                                        ('OFFICE_MANAGER', 'Office Manager'),
                                        ('STAFF', 'Staff'),
                                        ('RESIDENT_ADVISOR', 'Resident Advisor')])
