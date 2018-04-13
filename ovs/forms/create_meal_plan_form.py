""" Form with data required to create a meal plan """
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email

from ovs.forms.validators import EmailRegistered


class CreateMealPlanForm(FlaskForm):
    """ Form with data required to register a resident """
    email = StringField('User Email Address', validators=[Email(), DataRequired(),
                                                          EmailRegistered(True)])
    meal_plan = IntegerField('Meal Plan', validators=[DataRequired()])
    plan_type = SelectField('Plan Type', choices=[('WEEKLY', 'Weekly'),
                                                  ('SEMESTERLY', 'Semesterly'),
                                                  ('LIFETIME', 'Lifetime')])

    def validate_email(form, field):  # pylint: disable=no-self-argument
        """ Validates that this email doesn't already have a mealplan. """
        # TODO: Once meals get moved to users. Check if this account doesn't already have a mealplan.
        pass
