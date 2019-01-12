from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms.fields.html5 import EmailField

class RegisterForm(FlaskForm):
    first_name = StringField("First Name", [DataRequired(), Length(max=255)])
    last_name = StringField("Last Name", [DataRequired(), Length(max=255)])
    email = EmailField("Email", [DataRequired(), Email()])
    password = PasswordField("Password", [DataRequired(), Length(min=3)]) # Don't forget to set min=8
    confirm_password = PasswordField("Confirm password", [DataRequired(), EqualTo('password')])
    # captcha = RecaptchaField()
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = EmailField("Email", [DataRequired(), Email()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Log in")
