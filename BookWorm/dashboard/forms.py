from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length

class CreateNote(FlaskForm):
    text = HiddenField("note", [DataRequired()])
    submit = SubmitField("Save")

class UpdateNote(FlaskForm):
    text = HiddenField("note", [DataRequired()])
    submit = SubmitField("Save")
