""" Form with data to edit the current user's profile """
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, ValidationError
from wtforms.validators import Length, Email, DataRequired, optional
from wtforms.fields.html5 import TelField
import phonenumbers

from ovs.utils import genders


class EditResidentProfileForm(FlaskForm):
    """ Form with data to edit the current user's profile """
    preferred_name = StringField('Preferred Name', validators=[Length(max=255), DataRequired()])
    phone_number = TelField('Phone Number', validators=[optional()])
    preferred_email = StringField('Preferred Contact Email', validators=[Email(), Length(max=255)])
    race = StringField('Race/Ethnicity', validators=[Length(max=31)])
    gender = RadioField('Gender', choices=[(genders.MALE, 'Male'),
                                           (genders.FEMALE, 'Female'),
                                           (genders.UNSPECIFIED, 'Unspecified')])

    def validate_phone_number(form, field): # pylint: disable=no-self-argument, no-self-use
        """
        Validates that the provided phone number is valid.
        """
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(field.data)
            if not phonenumbers.is_valid_number(input_number):
                raise ValidationError('Invalid phone number.')
            #phonenumbers.phonenumberutil.NumberParseException could happen
        except: #pylint: disable=bare-except
            try: #Try to add the US area code to it
                input_number = phonenumbers.parse("+1"+field.data)
                if not phonenumbers.is_valid_number(input_number):
                    raise ValidationError('Invalid phone number.')
            except: #pylint: disable=bare-except
                raise ValidationError('Invalid phone number.')
