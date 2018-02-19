""" Form with data required to register a resident """
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class RegisterResidentForm(FlaskForm):
    """ Form with data required to register a resident """
    email = StringField('Email Address', validators=[Length(min=6, max=35), DataRequired()])
    first_name = StringField('First Name', validators=[Length(min=1, max=255), DataRequired()])
    last_name = StringField('Last Name', validators=[Length(min=1, max=255), DataRequired()])
