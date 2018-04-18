""" routes under /auth/ """
import logging
import traceback

from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, login_required

from ovs import db
from ovs.forms.login_form import LoginForm
from ovs.forms import ResetRequestForm, ResetPasswordForm
from ovs.services import AuthService
from ovs.utils.roles import UserRole
from ovs.utils import serializer
from ovs.services.user_service import UserService

auth_bp = Blueprint('auth', __name__, )


@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    """ Interface for users to login """
    try:
        login_form = LoginForm()
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data
            user = UserService.get_user_by_email(email)
            if user is None:
                flash('Invalid email or password.', 'danger')
                return redirect(url_for('/.landing_page'))
            elif not AuthService.verify_auth(user, password):
                flash('Invalid email or password.', 'danger')
                return redirect(url_for('/.landing_page'))
            login_user(user)
            db.session.commit()
            if user.role == UserRole.RESIDENT:
                return redirect(url_for('resident.landing_page'))
            else:
                return redirect(url_for('manager.landing_page'))

        return render_template('login.html', login_form=login_form)
    except:  # pylint: disable=bare-except
        db.session.rollback()
        flash('Could not log in', 'danger')
        logging.exception(traceback.format_exc())
        return redirect(url_for('/.landing_page'))

@auth_bp.route('/reset/', methods=['GET', 'POST'])
def request_user_reset():
    """ Allows a user to send a password reset request."""
    try:
        form = ResetRequestForm()
        if form.validate_on_submit():
            UserService.send_reset_email(form.email.data)
            flash('Sent reset email!', 'success')
            return redirect(url_for('auth.login'))

        return render_template('reset_request.html', form=form)
    except:  # pylint: disable=bare-except
        db.session.rollback()
        flash('An error was encountered.', 'danger')
        logging.exception(traceback.format_exc())
        return redirect(url_for('auth.login'))

@auth_bp.route('/reset/<token>/', methods=['GET', 'POST'])
def reset_user(token):
    """Allows a user with a valid token to reset their password."""
    try:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            email = serializer.decode_attr(token, 'ovs-reset-email')

            user = UserService.get_user_by_email(email)
            UserService.reset_user(user, form.password.data)
            db.session.commit()
            flash('Successfully updated password!', 'success')
            return redirect(url_for('/.landing_page'))

        return render_template('reset_password.html', form=form)
    except:  # pylint: disable=bare-except
        db.session.rollback()
        flash('An error was encountered', 'danger')
        logging.exception(traceback.format_exc())
        return redirect(url_for('auth.login'))

@auth_bp.route('/logout/')
@login_required
def logout():
    """ Logs a user out """
    try:
        logout_user()
        return redirect(url_for('/.landing_page'))
    except:  # pylint: disable=bare-except
        db.session.rollback()
        flash('An error was encountered', 'danger')
        logging.exception(traceback.format_exc())
        return redirect(url_for('/.landing_page'))
