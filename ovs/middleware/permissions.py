"""Middleware to allow for user role based endpoint control"""
from flask_login import current_user
from flask import flash, redirect, url_for
from ovs.utils import roles

class Permissions(object):
    """Permissions decorator to allow for role based endpoint control"""
    def __init__(self, role):
        self.role = role

    def __call__(self, func):
        # pylint: disable=missing-docstring
        def authorize_and_call(*args, **kwargs):
            if not roles.has_permission(current_user.role, self.role):
                flash('Unauthorized Access!')
                return redirect(url_for('/.landing_page'))
            return func(*args, **kwargs)
        return authorize_and_call
