from functools import wraps
from flask_login import current_user
from ovs.utils import roles
from flask import flash, redirect, url_for

class Permissions(object):
    def __init__(self, role):
        self.role = role
    def __call__(self, func):
        def authorize_and_call(*args, **kwargs):
            if not roles.has_permission(current_user.role, self.role):
                flash('Unauthorized Access!')
                return redirect(url_for('/.landing_page'))
            return func(*args, **kwargs)
        return authorize_and_call
