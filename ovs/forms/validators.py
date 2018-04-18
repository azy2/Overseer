""" Validators for reuse in forms """
from wtforms import ValidationError

from ovs.services.user_service import UserService

class EmailRegistered(object):
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
        """ Does the validation """
        email = field.data.strip()
        user = UserService.get_user_by_email(email)
        not_registered = user is None
        if not_registered == self.check:
            raise ValidationError(self.message)
