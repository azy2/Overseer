""" Form with data required to login for a meal"""
from flask_wtf import FlaskForm
from wtforms import IntegerField, ValidationError
from wtforms.validators import DataRequired
from ovs.models.meal_plan_model import MealPlan
from ovs import app
db = app.database.instance()

def validate_meal_pin(form, field):  # pylint: disable=unused-argument
    """
    Validates that the provided pin existsself.
    This is to thwart malicious input.
    """
    if db.query(MealPlan).filter(MealPlan.pin == field.data).count() == 0:
        raise ValidationError('Invalid Pin')


class MealLoginForm(FlaskForm):
    """ Form with data required to login for a meal"""
    pin = IntegerField('PIN', validators=[DataRequired(), validate_meal_pin])