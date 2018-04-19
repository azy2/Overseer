""" Validators for reuse in forms """
from wtforms import ValidationError

from ovs.services.user_service import UserService

class EmailRegistered(object):
    """
    Validates that an email is or is not registered.

    Args:
        check: Whether to validate that the email is registered or unregistered.
        message (str, optional): The message to be displayed to the user on the form if the check fails.
                                 If no message is provided the message will either be:
                                 "Email must be an existing user" or
                                 "Email already in use"
    """
    """ If check is true validates that the given email is registered.
        If check is false validates that the given email is unregistered.
        If the validation is failed message will be displayed.
        If message is ommitted 'Email must be an existing user' is printed for check=True
        and 'Email already in use' is printed for check=False """

    def __init__(self, check, message=None):
        """ Recieves paramaters for the validator """
        self.check = check
        if check and not message:
            message = "Email must be an existing user"
        elif not check and not message:
            message = "A user with that email already exists"
        self.message = message

    def __call__(self, form, field):
        """
        Does the validation.

        Args:
            form: The form this validator is applied to.
            field: The field this validator is applied to.

        Raises:
            ValidationError: If the given email is unregistered if check=True
                             and if the given email is registered if check=False.
        """
        user = UserService.get_user_by_email(field.data)
        not_registered = user is None
        if not_registered == self.check:
            raise ValidationError(self.message)
