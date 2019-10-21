from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField
from wtforms.validators import DataRequired, Length, Email
from wtforms.fields.html5 import EmailField


class EditNote(FlaskForm):
    text = HiddenField("note", [DataRequired()])
    submit = SubmitField("Save")


class EditProfile(FlaskForm):
    first_name = StringField("First Name", [DataRequired(), Length(max=50)])
    last_name = StringField("Last Name", [DataRequired(), Length(max=50)])
    email = EmailField("Email", [DataRequired(), Email()])
    submit = SubmitField("Update")

