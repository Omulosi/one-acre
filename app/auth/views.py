from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user
from . import auth_blueprint as auth
from .form import PasswordResetForm
from ..email import send_mail
from ..models import User
from .. import db


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(
                url_for('.password_reset'))  # front-end-host/home-page-url
        else:
            return redirect(
                url_for('.password_reset'))  # front-end-host/home-page-url
    return render_template('reset_password.html', form=form)
