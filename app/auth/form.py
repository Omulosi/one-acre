from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from ..models import User


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password',
                             validators=[
                                 DataRequired(),
                                 EqualTo('password2',
                                         message='Passwords must match')
                             ])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
