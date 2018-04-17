"""
DB and utility functions for Meals
"""

from ovs import db
from ovs.models.meal_plan_model import MealPlan
from ovs.models.mealplan_history_model import MealplanHistory
from ovs.utils import log_types


class MealService:
    """ DB and utility functions for Meals """

    @staticmethod
    def create_meal_plan(meal_plan, plan_type):
        """
        Adds a MealPlan db entry.

        Args:
            meal_plan: The plan's maximum credit.
            plan_type: The plan's reset period.

        Returns:
            A MealPlan db model.
        """
        new_plan = MealPlan(meal_plan, plan_type)
        db.session.add(new_plan)
        db.session.flush()
        return new_plan

    @staticmethod
    def create_meal_plan_for_resident_by_email(meal_plan, plan_type, email):
        """
        Create a new meal plan db entry
          and assign a meal plan pin to an existing resident identified by email.

        Args:
            meal_plan: The plan's maximum credit.
            plan_type: The plan's reset period.
            email: An email address.

        Returns:
            A MealPlan db model.
        """
        from ovs.services.resident_service import ResidentService

        resident = ResidentService.get_resident_by_email(email)
        meal_plan = MealService.create_meal_plan(meal_plan, plan_type)
        resident.mealplan_pin = meal_plan.pin
        db.session.flush()
        db.session.refresh(resident)
        return meal_plan

    @staticmethod
    def use_meal(pin, manager_id):
        """
        Decrement credit for meal plan identified by meal pin
          and log a MealService db entry.

        Args:
            pin: Unique meal pin.
            manager_id: Unique user id.

        Returns:
            If the meal credit was deducted and logged succesfully.
        """
        from ovs.services.resident_service import ResidentService

        mealplan = MealService.get_meal_plan_by_pin(pin)
        resident = ResidentService.get_resident_by_pin(pin)
        if mealplan.update_meal_count():
            MealService.log_meal_history(resident.user_id, mealplan.pin, manager_id, log_types.MEAL_USED)
            return True
        else:
            return False

    @staticmethod
    def add_meals(pin, number):
        """
        Add credits to meal plan identified by meal pin.

        Args:
            pin: Unique meal pin.
            number: The number of credits to add.

        Returns:
            If the credits were added successfully.
        """
        meal_plan = MealService.get_meal_plan_by_pin(pin)
        meal_plan.credits += number
        db.session.flush()
        db.session.refresh(meal_plan)

    @staticmethod
    def undo_meal_use(manager_id, resident_id, pin):
        """
        Adds a single credit back to meal plan identified by meal pin
          and adds a MealService db entry.

        Args:
            manager_id: Unique user id that identifies the manager that authorized the undo.
            resident_id: Unique id that identifies the resident that the meal plan is associated with.
            pin: Unique meal pin.

        Returns:
            If the credit and loggs was added successfully.
        """
        MealService.add_meals(pin, 1)
        MealService.log_meal_history(resident_id, pin, manager_id, log_types.UNDO)

    @staticmethod
    def get_meal_plan_by_pin(pin):
        """
        Fetch the mean plan that is associated with the meal pin.

        Args:
            pin: Unique meal pin.

        Returns:
            A MealPlan db model.
        """
        return db.session.query(MealPlan).filter_by(pin=pin).first()

    @staticmethod
    def log_meal_history(resident_id, pin, manager_id, log_type):
        """
        Adds a MealPlanHistory to db that logs the login/undo action.

        Args:
            resident_id: Unique resident id that identifies the user that the meal plan is associated with.
            pin: Unique meal pin.
            manager_id: Unique user id that identifies the manager that authorized the undo action.
            log_type: log_types.MEAL_USED or log_types.UNDO

        Returns:
            If the meal history was logged successfully.
        """
        new_mealplan_history_item = MealplanHistory(
            resident_id, pin, manager_id, log_type)
        db.session.add(new_mealplan_history_item)
        db.session.flush()

    @staticmethod
    def get_last_log(manager_id):
        """
        Fetch the most recent meal log associated manager identified by manager id.

        Args:
            manager_id: Unique user id.

        Returns:
            A MealPlanHistory db model.
        """
        return db.session.query(MealplanHistory).filter_by(manager_id=manager_id)\
                                                .order_by(MealplanHistory.id.desc()).first()

    @staticmethod
    def get_logs():
        """
        Returns a list of all meal logs.

        Returns:
            A list of MealPlanHistory db model.
        """
        return db.session.query(MealplanHistory).order_by(MealplanHistory.id.desc()).all()
