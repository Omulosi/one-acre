from flask import render_template, redirect, url_for, flash, current_app
from . import auth_blueprint as auth
from .form import PasswordResetForm
from ..email import send_mail
from ..models import User
from .. import db


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    form = PasswordResetForm()
    app = current_app._get_current_object()
    frontend_login_url = app.config['FRONT_END_HOST'] + '/login'
    if form.validate_on_submit():
        print("Inside password_reset view")
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('.password_reset', token=token))
    return render_template('reset_password.html',
                           form=form,
                           login_url=frontend_login_url)
