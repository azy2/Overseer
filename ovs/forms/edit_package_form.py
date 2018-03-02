""" Form with data required to edit a resident """
from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired, Length
from ovs.models.resident_model import Resident
from ovs.models.package_model import Package
from ovs import app
db = app.database.instance()


def validate_user_id(form, field):  # pylint: disable=unused-argument
    """
    Validates that the provided user_id exists.
    This is to thwart malicious input.
    """
    if db.query(Resident).filter(Resident.user_id == field.data).count() == 0:
        raise ValidationError('Resident does not exist')

def validate_package_id(form, field):  # pylint: disable=unused-argument
    """
    Validates that the provided user_id exists.
    This is to thwart malicious input.
    """
    if db.query(Package).filter(Package.id == field.data).count() == 0:
        raise ValidationError('Package does not exist')

class EditPackageForm(FlaskForm): # NEED MORE VALIDATORS? !!!
    package_id = StringField('Package ID', validators=[DataRequired(), validate_package_id]) # (hidden)
    user_id = StringField('User ID', validators=[DataRequired(), validate_user_id]) # (hidden)
    email = StringField('Reciever\'s Email Address', validators=[Length(min=6, max=35), DataRequired()]) # (editable)
    checked_by = StringField('Checked By', validators=[DataRequired()])
    checked_at = StringField('Checked At', validators=[DataRequired()])
    is_signed = StringField('Is Signed', validators=[DataRequired()])
    signed_at = StringField('Signed At', validators=[DataRequired()])
    description = StringField('Package Description', validators=[Length(min=0, max=2047), DataRequired()]) # (editable)