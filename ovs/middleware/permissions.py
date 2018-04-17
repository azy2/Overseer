"""Middleware to allow for user role based endpoint control"""
from functools import wraps
from flask_login import current_user
from flask import flash, redirect, request
from ovs.utils import roles


class Permissions(object):
    """
    Requires that the user who accesses the decorated route has the correct permissions.
    Args:
        role: The minimum role required to access this route.

    Returns:
        A func that does the permission checking.

    Examples:
        routes that need authorization should apply the decorator like so:

        from ovs.middleware import permissions
        @bp.route('/my_admin_only_route/', methods=['GET'])
        @permissions(roles.ADMIN)
        def my_admin_only_route():
            ...
    """
    def __init__(self, role):
        self.role = role

    def __call__(self, func):
        """
        This function is an implementation detail of decorators.
        See :class:`ovs.middleware.Permissions`
        Args:
            func: The decorated function.

        Returns:
            A function handled by python.
        """
        @wraps(func)
        def authorize_and_call(*args, **kwargs):
            """
            This is an inner function of `Permissions.__call__` which is required for python decorators.
            Args:
                *args: Handled by python
                **kwargs: Handled by python

            Returns:
                A parameterized decorator.
            """
            if not roles.has_permission(current_user.role, self.role):
                flash('Unauthorized Access!', 'danger')
                print(request.referrer)
                return redirect(request.referrer or '/')
            return func(*args, **kwargs)
        return authorize_and_call
