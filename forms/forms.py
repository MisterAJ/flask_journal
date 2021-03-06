from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, \
    Length, EqualTo

from models import user
User = user.User


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("User already exists")


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("Email already exists")


class RegisterForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message='Only one word with no fancy stuff'
            ),
            name_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()])
