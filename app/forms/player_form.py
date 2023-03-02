from wtforms.validators import DataRequired, Length
from wtforms import StringField, SubmitField, IntegerField
from flask_wtf import FlaskForm
from flask import session


class NumberOfPlayers(FlaskForm):
    num_players = IntegerField(
        label='How many people are playing?',
        validators=[DataRequired()]
    )

    submit = SubmitField(label="Let's Play")


class PlayerNames(FlaskForm):

    submit = SubmitField(label='Get Started')
