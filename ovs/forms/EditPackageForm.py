from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import Length, DataRequired

class EditPackageForm(FlaskForm):
    email = StringField('Email Address', validators=[Length(min=6, max=35), DataRequired()])
    description = StringField('Description', validators=[Length(min=0, max=2047)])