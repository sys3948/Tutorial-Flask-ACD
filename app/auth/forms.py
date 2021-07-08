from flask.globals import request
from wtforms import validators
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])

    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames musthave only letters, numbers, dots or underscores')])
    password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[Required()])
    password = PasswordField('New Password Field', validators=[Required(), EqualTo('password2', message='Password must match.')])
    password2 = PasswordField('Confirm new Password', validators=[Required()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Reset Password', validators=[Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm Password', validators=[Required()])
    submit = SubmitField('Reset Password')


class ChangeEmailForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Update Email Address')