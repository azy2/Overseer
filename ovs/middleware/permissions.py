"""Middleware to allow for user role based endpoint control"""
from functools import wraps
from flask_login import current_user
from flask import flash, redirect, request
from ovs.utils import roles

class Permissions(object):
    """Permissions decorator to allow for role based endpoint control"""
    def __init__(self, role):
        self.role = role

    def __call__(self, func):
        """Calls the decorator function"""
        @wraps(func)
        def authorize_and_call(*args, **kwargs):
        """Calls the decorated function on successful perm check"""
            if not roles.has_permission(current_user.role, self.role):
                flash('Unauthorized Access!', 'error')
                print(request.referrer)
                return redirect(request.referrer or '/')
            return func(*args, **kwargs)
        return authorize_and_call
