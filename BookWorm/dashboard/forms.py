from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length

class CreateNote(FlaskForm):
    title = StringField("Title", [DataRequired(), Length(max=255)])
    text = HiddenField("Note", [DataRequired()])
    submit = SubmitField("Submit")
