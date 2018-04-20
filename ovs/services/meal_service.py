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

        ResidentService.set_resident_pin(resident.user_id, meal_plan.pin)
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

        return False

    @staticmethod
    def edit_meal_plan(pin, credit=None, plan_meal_count=None, plan_type=None):
        """
        Updates a meal plan with any provided info.

        Args:
            pin: Unique meal pin.
            credit: Number of credits until the next reset_date.
            plan_meal_count: Number of meals given at each reset_date.
            plan_type: The plans reset period.
        """
        meal_plan = MealService.get_meal_plan_by_pin(pin)
        if credit:
            meal_plan.credits = credit
        if plan_meal_count:
            meal_plan.meal_plan = plan_meal_count
        if plan_type:
            meal_plan.plan_type = plan_type
        meal_plan.reset_date = meal_plan.get_next_reset_date()
        db.session.flush()


    @staticmethod
    def add_meals(pin, number):
        """
        Add credits to meal plan identified by meal pin.

        Args:
            pin: Unique meal pin.
            number: The number of credits to add.
        """
        meal_plan = MealService.get_meal_plan_by_pin(pin)
        MealService.edit_meal_plan(pin, credit=meal_plan.credits+number)

    @staticmethod
    def delete_meal_plan(pin):
        """
        Deletes a meal plan from the database.

        Args:
            pin: Unique meal pin.
        """
        from ovs.services.resident_service import ResidentService
        meal_plan = MealService.get_meal_plan_by_pin(pin)

        resident = ResidentService.get_resident_by_pin(meal_plan.pin)
        ResidentService.set_resident_pin(resident.user_id, 0)

        db.session.delete(meal_plan)
        db.session.flush()


    @staticmethod
    def undo_meal_use(manager_id, resident_id, pin):
        """
        Adds a single credit back to meal plan identified by meal pin
          and adds a MealService db entry.

        Args:
            manager_id: Unique user id that identifies the manager that authorized the undo.
            resident_id: Unique id that identifies the resident that the meal plan is associated with.
            pin: Unique meal pin.
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

        meal_plan = db.session.query(MealPlan).filter_by(pin=pin).first()
        if meal_plan is not None:
            meal_plan.check_reset_date() #update this lazy evaluation
        return meal_plan

    @staticmethod
    def get_all_meal_plans():
        """
        Fetch all meal plans in the database

        Returns:
            A list of MealPlan db models.
        """
        meal_plans = db.session.query(MealPlan).all()
        for meal_plan in meal_plans:
            meal_plan.check_reset_date() #update this lazy evaluation
        return meal_plans

    @staticmethod
    def log_meal_history(resident_id, pin, manager_id, log_type):
        """
        Adds a MealPlanHistory to db that logs the login/undo action.

        Args:
            resident_id: Unique resident id that identifies the user that the meal plan is associated with.
            pin: Unique meal pin.
            manager_id: Unique user id that identifies the manager that authorized the undo action.
            log_type: log_types.MEAL_USED or log_types.UNDO
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

    @staticmethod
    def get_log_to_undo(undo_date, manager_id):
        """
        Get the meal log corresponding to the given undo for a specific manager.

        Args:
            undo_data: Datetime of undo
            manager_id: User id of manager who logged the meal that is being undone.

        Returns:
            A MealPlanHistory db model.
        """
        return db.session.query(MealplanHistory).filter(MealplanHistory.created < undo_date)\
                                                .filter_by(manager_id=manager_id)\
                                                .order_by(MealplanHistory.id.desc()).first()

    @staticmethod
    def get_aggregate_meal_usage():
        """
        Gets a list of the number of meals used for each hour.

        Returns:
            List of length 24 with each element representing an hour and its value being the
            average number of meals used for that hour over all days in the meal history.
        """

        # Initialize variables
        history = MealService.get_logs()

        aggregate_meal_usage = [0 for i in range(24)]
        curr_meal_usage = [0 for i in range(24)]
        day_count = 1
        curr_day = None
        prev_hour = None

        # Loop through every log in meal history
        for log in history:
            # Update meal usage for the given day and hour
            if log.log_type == "MEAL_USED":
                # Initialize log variables
                hour = log.created.hour
                prev_hour = hour
                log_day = [log.created.month, log.created.day, log.created.year]

                # Current day not yet set (first log)
                if curr_day == None:
                    curr_day = log_day

                # Current day has changed, update aggregate values
                if curr_day != log_day:
                    for i in range(24):
                        aggregate_meal_usage[i] = (aggregate_meal_usage[i] + curr_meal_usage[i]) / day_count
                    curr_meal_usage = [0 for i in range(24)]
                    curr_day = log_day
                    day_count += 1

                # Increment current day's meal usage for the log's hour
                curr_meal_usage[hour-1] += 1

            # Remove the previous meal from the usage stats
            elif log.log_type == "UNDO":
                bad_log = MealService.get_log_to_undo(log.created, log.manager_id)
                curr_meal_usage[bad_log.created.hour-1] -= 1

        # Final update for last day
        for i in range(24):
            aggregate_meal_usage[i] = (aggregate_meal_usage[i] + curr_meal_usage[i]) / day_count

        return aggregate_meal_usage
