from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField
from wtforms.validators import DataRequired


class EditNote(FlaskForm):
    text = HiddenField("note", [DataRequired()])
    submit = SubmitField("Save")
