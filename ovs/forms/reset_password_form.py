"""Form to validate password resets."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, validators

class ResetPasswordForm(FlaskForm):
    """Form to validate password resets."""
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
