""" Form with data required to create a meal plan """
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, ValidationError
from wtforms.validators import DataRequired, Email, NumberRange

from ovs import db

from ovs.models.resident_model import Resident
from ovs.models.user_model import User


class CreateMealPlanForm(FlaskForm):
    """ Form with data required to register a resident """
    email = StringField('User Email Address', validators=[Email(), DataRequired()])
    meal_plan = IntegerField('Meal Plan', validators=[NumberRange(min=1)])
    plan_type = SelectField('Plan Type', choices=[('WEEKLY', 'Weekly'),
                                                  ('SEMESTERLY', 'Semesterly'),
                                                  ('LIFETIME', 'Lifetime')])

    def validate_email(form, field):  # pylint: disable=no-self-argument, no-self-use
        """
        Validates that this email doesn't already have a mealplan.

        Args:
            form: The CreateMealPlanForm that was submitted.
            field: The email field.

        Raises:
            ValidationError: If email does not correspond to an existing account
                             or if the account does not have a meal plan.
         """
        resident_user = db.session.query(Resident, User).join(User, Resident.user_id == User.id)\
                                           .filter(User.email == field.data).first()
        if resident_user is None:
            raise ValidationError('Resident does not exist. Please verify resident email.')
        if resident_user[0].mealplan_pin is not 0:
            raise ValidationError('Resident has a meal plan.')
