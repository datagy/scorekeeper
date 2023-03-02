from wtforms.validators import DataRequired, Length
from wtforms import StringField, SubmitField, IntegerField
from flask_wtf import FlaskForm
from flask import session


class ScoreForm(FlaskForm):
    submit = SubmitField(label="Submit Scores")
