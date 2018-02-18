from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators

class RegisterManagerForm(FlaskForm):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.DataRequired()])
    first_name = StringField('First Name', [validators.Length(min=1, max=255), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=255), validators.DataRequired()])
    role = SelectField('Role', choices=[('ADMIN', 'Admin'),
                                        ('BUILDING_MANAGER', 'Bulding Manager'),
                                        ('OFFICE_MANAGER', 'Office Manager'),
                                        ('STAFF', 'Staff'),
                                        ('RESIDENT_ADVISOR', 'Resident Advisor')])

