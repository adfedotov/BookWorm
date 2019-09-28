from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    first_name = StringField("First Name", [DataRequired(), Length(max=50)])
    last_name = StringField("Last Name", [DataRequired(), Length(max=50)])
    email = EmailField("Email", [DataRequired(), Email()])
    password = PasswordField("Password", [DataRequired(), Length(min=5)])  # TODO: Connect to config
    confirm_password = PasswordField("Confirm password", [DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = EmailField("Email", [DataRequired(), Email()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Log in")
