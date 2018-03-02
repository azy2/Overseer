from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import Length, DataRequired

class AddPackageForm(FlaskForm):
    email = StringField('Receiver\'s Email Address', validators=[Length(min=6, max=35), DataRequired()])
    description = StringField('Package Description', validators=[Length(min=0, max=2047)])