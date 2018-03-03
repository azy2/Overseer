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
    gender = RadioField('Gender', choices=[('1', 'Male'), ('2', 'Female'), ('3', 'Unspecified')])

##    def __init__(self, profile_to_edit, **kwargs):
##        super(EditResidentProfileForm, self).__init__(self, **kwargs)
        
""" 
    def __init__(self, profile_to_edit):#, *args, **kwargs):       
        # Set default field values based on existing profile
        if(profile_to_edit.preferred_name):
            preferred_name.default = profile_to_edit.preferred_name

        if(profile_to_edit.phone_number):
            phone_number.default = profile_to_edit.phone_number
 
       if(profile_to_edit.preferred_email):
            preferred_email.default = profile_to_edit.preferred_email

        if(profile_to_edit.race):
            race.default = profile_to_edit.race

        # If gender is null, set radio button to unspecified
        #gender.default = '3'
        #if(profile_to_edit.gender):
        #    if(profile_to_edit.gender == genders.MALE):
        #        gender.default = '1'
        #    else:
        #        gender.default = '2'

        #super().__init__(self, *args, **kwargs)
"""
