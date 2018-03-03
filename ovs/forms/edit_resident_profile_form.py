""" Form with data to edit the current user's profile """
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import Length, Email
from ovs.utils import genders

class EditResidentProfileForm(FlaskForm):
    """ Form with data to edit the current user's profile """
    preferred_name = StringField('Preferred Name', validators=[Length(max=255)])
    phone_number = StringField('Phone Number', validators=[Length(max=31)])
    preferred_email = StringField('Preferred Contact Email', validators=[Email(), Length(max=255)])
    race = StringField('Race/Ethnicity', validators=[Length(max=31)])
    gender = RadioField('Gender', choices=[(genders.MALE, 'Male'), (genders.FEMALE, 'Female'), (None, 'Unspecified')])

#    def __init__(self, profile_to_edit, **kwargs):
#        super(EditResidentProfileForm, self).__init__(self, **kwargs)
