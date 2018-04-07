""" routes under /auth/ """
from flask import Blueprint, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required

from ovs.forms.login_form import LoginForm
from ovs.services import AuthService
from ovs.utils.roles import UserRole
from ovs.services.user_service import UserService

auth_bp = Blueprint('auth', __name__, )
db = current_app.extensions['database'].instance()


@auth_bp.route('/login', methods=['POST'])
def login():
    """ Interface for users to login """
    form = LoginForm()
    if form.validate():
        email = form.email.data
        password = form.password.data
        user = UserService.get_user_by_email(email).one_or_none()
        if user is None:
            flash('Invalid Email.', 'error')
            return redirect(url_for('/.landing_page'))
        elif not AuthService.verify_auth(user, password):
            flash('Invalid password.', 'error')
            return redirect(url_for('/.landing_page'))
        login_user(user)
        if user.role == UserRole.RESIDENT:
            return redirect(url_for('resident.landing_page'))
        else:
            return redirect(url_for('manager.landing_page'))
    else:
        return str(form.errors)


@auth_bp.route('/logout')
@login_required
def logout():
    """ Logs a user out """
    logout_user()
    return redirect(url_for('/.landing_page'))
