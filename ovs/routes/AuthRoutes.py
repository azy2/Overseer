from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required

from ovs import app
from ovs.forms.LoginForm import LoginForm
from ovs.logging import Logger
from ovs.models.UserModel import User

auth_bp = Blueprint('auth', __name__,)
db = app.database.instance()


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        # TODO: validate passwords once user is able to reset them.
        # password = form.password.data
        user = db.query(User).filter_by(email=email).first()
        if user is None:
            flash('Invalid Credentials.', 'error')
            return redirect(url_for('auth.login'))
        login_user(user)
        flash('success!', 'message')
        return redirect(url_for('auth.login'))
    return render_template('login_page.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/test')
@login_required
def test():
    return 'I am logged in.'
