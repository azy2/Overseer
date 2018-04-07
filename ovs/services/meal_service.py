"""
DB and utility functions for Meals
"""
from datetime import datetime

from flask import current_app

from ovs.models.mealplan_history_model import MealplanHistory
from ovs.models.meal_plan_model import MealPlan
from ovs.utils import log_types


db = current_app.extensions['database'].instance()


class MealService:
    """ DB and utility functions for Meals """

    def __init__(self):
        pass

    @staticmethod
    def create_meal_plan(meal_plan, plan_type):
        """
        Adds a new meal plan to the DB
        :param pin: The plan's pin
        :param meal_plan: The plan's maximum credit count
        :param plan_type: The plan's reset period
        :return: True for success, False for failure
        """
        new_plan = MealPlan(meal_plan, plan_type)
        db.add(new_plan)
        db.commit()
        return new_plan

    @staticmethod
    def add_meals(pin, number):
        """
        Add numbers of meal credits
        :param pin: The plan's pin
        :type pin: int
        :param number: Number of credits
        :type number: int
        :return: validity of adding
        :rtype: bool
        """
        meal_plan = MealService.get_meal_plan_by_pin(pin)
        if meal_plan is None:
            return False
        meal_plan.credits += number
        db.commit()
        return True

    @staticmethod
    def update_meal_count(meal_plan):
        """
        Reset meal plan credits if past reset data
        Decrement meal plan credits if available
        Commit changes to DB
        :param meal_plan:
        :type meal_plan:
        :return: whether a credit was available
        :rtype: bool
        """
        if meal_plan.reset_date is None or datetime.utcnow() > meal_plan.reset_date:
            meal_plan.reset_date = meal_plan.get_next_reset_date()
            meal_plan.credits = meal_plan.meal_plan
        was_updated = False
        if meal_plan.credits > 0:
            meal_plan.credits -= 1
            was_updated = True
        db.commit()
        return was_updated

    @staticmethod
    def undo_meal_use(manager_id, resident_id, pin):
        """
        Reverts the usage of a meal logged by the given manager
        :param manager_id: id for the manager who logged the resident's usage of a meal and wishes to undo that
        :param resident_id: id for the resident who has the meal plan
        :param pin: the pin of the meal plan to be reverted
        :return: True if successful
        """
        if not MealService.add_meals(pin, 1):
            return False
        MealService.log_undo_meal_use(resident_id, pin, manager_id)
        return True

    @staticmethod
    def get_meal_plan_by_pin(pin):
        """
        Gets the account with given pin
        :param pin: account to use
        :return: The account
        """
        return db.query(MealPlan).filter(MealPlan.pin == pin).first()

    @staticmethod
    def log_meal_use(resident_id, pin, manager_id):
        """
        Logs a meal use on the given account
        :param resident_id: id for the given resident
        :param pin: PIN for the given resident's mealplan
        :param manager_id: id for the manager logging the resident's usage of a meal
        """
        new_mealplan_history_item = MealplanHistory(resident_id, pin, manager_id, log_types.MEAL_USED)
        db.add(new_mealplan_history_item)
        db.commit()

    @staticmethod
    def log_undo_meal_use(resident_id, pin, manager_id):
        """
        Logs the undo of a meal use logged by the given manager
        :param resident_id: id for the given resident
        :param pin: PIN for the given resident's mealplan
        :param manager_id: id for the manager who logged the resident's usage of a meal and wishes to undo that
        """
        new_mealplan_history_item = MealplanHistory(resident_id, pin, manager_id, log_types.UNDO)
        db.add(new_mealplan_history_item)
        db.commit()

    @staticmethod
    def get_last_log(manager_id):
        """
        Get the last meal log logged by this manager
        :param manager_id: id of manager
        :return: latest row logged in the meal plan history table or None
        """
        meal_log = db.query(MealplanHistory).filter(manager_id).order_by(MealplanHistory.id.desc()).first()
        return meal_log
