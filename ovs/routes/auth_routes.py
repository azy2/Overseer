""" routes under /auth/ """
from flask import Blueprint, redirect, url_for, flash, request, render_template, abort
from flask_login import login_user, logout_user, login_required
from itsdangerous import SignatureExpired, BadTimeSignature, BadSignature

from ovs.forms.login_form import LoginForm
from ovs.forms import ResetRequestForm, ResetPasswordForm
from ovs.services import AuthService
from ovs.utils.roles import UserRole
from ovs.utils import serializer
from ovs.services.user_service import UserService

auth_bp = Blueprint('auth', __name__, )


@auth_bp.route('/login', methods=['POST'])
def login():
    """ Interface for users to login """
    form = LoginForm()
    if form.validate():
        email = form.email.data
        password = form.password.data
        user = UserService.get_user_by_email(email)
        if user is None:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('/.landing_page'))
        elif not AuthService.verify_auth(user, password):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('/.landing_page'))
        login_user(user)
        if user.role == UserRole.RESIDENT:
            return redirect(url_for('resident.landing_page'))
        else:
            return redirect(url_for('manager.landing_page'))
    else:
        flash('Invalid email or password.', 'danger')
        return redirect(url_for('/.landing_page'))

@auth_bp.route('/user/reset', methods=['GET', 'POST'])
def request_user_reset():
    """ Allows a user to send a password reset request."""
    form = ResetRequestForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = UserService.get_user_by_email(form.email.data)
            if not user:
                flash('Invalid email', 'error')
            else:
                UserService.send_reset_email(form.email.data)
                flash('Sent reset email!', 'success')
            return redirect(url_for('/.landing_page'))

    return render_template('reset_request_page.html', form=form)

@auth_bp.route('/reset/<token>', methods=['GET', 'POST'])
def reset_user(token):
    """Allows a user with a valid token to reset their password."""
    form = ResetPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                email = serializer.decode_attr(token, 'ovs-reset-email')
            except (SignatureExpired, BadTimeSignature, BadSignature) as _:
                abort(404)

            user = UserService.get_user_by_email(email)
            UserService.reset_user(user, form.password.data)
            flash('Successfully updated password!', 'message')
            return redirect(url_for('/.landing_page'))
        else:
            flash('Passwords must match', 'error')
            return redirect(url_for('auth.reset_user', token=token))
    else:
        return render_template('reset_password_page.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """ Logs a user out """
    logout_user()
    return redirect(url_for('/.landing_page'))
