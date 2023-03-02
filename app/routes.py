from flask import render_template, redirect, url_for, session
from app import app
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

from app.forms.player_form import NumberOfPlayers, PlayerNames
from app.forms.scores_form import ScoreForm

import pandas as pd


def calculate_cumulative_scores(values):
    vals = [i[1] for i in values]
    rounds = [i[0] for i in values]

    df = pd.DataFrame(vals)
    cumulative_vals = df.cumsum().values.tolist()

    cumulative_scores = list(zip(rounds, cumulative_vals))

    return cumulative_scores


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NumberOfPlayers()

    if form.validate_on_submit():
        session.clear()
        session['scores'] = []
        session['round'] = 0
        session['num_players'] = form.data['num_players']
        return redirect(url_for('names'))
    return render_template('index.html', form=form)


@app.route('/names', methods=['GET', 'POST'])
def names():
    num_players = session.get('num_players')
    for i in range(1, num_players + 1):
        player_num = f'player{i}'
        player_label = f'Player {i}'
        setattr(PlayerNames, player_num, StringField(
            label=player_label, validators=[DataRequired()]))
    form = PlayerNames()

    if form.validate_on_submit():
        players = [v for k, v in form.data.items() if 'player' in k]
        session['players'] = list(sorted(players))

        return redirect(url_for('scores'))

    return render_template('names.html', form=form)


@app.route('/scores', methods=['GET', 'POST'])
def scores():
    players = session['players'].copy()

    for name in players:
        setattr(ScoreForm, name, IntegerField(
            label=name, validators=[DataRequired()]))
    form = ScoreForm()

    table_cols = ['Round'] + players
    table_values = []
    cumulative_scores = []

    if form.validate_on_submit():
        scores = {k: v for k, v in form.data.items() if k in players}
        scores['round'] = session['round']
        session['round'] += 1
        session['scores'].append(scores)

        for idx, round in enumerate(session['scores'], start=1):
            sorted_round = [round.get(player) for player in session['players']]
            table_values.append([idx, sorted_round])

        cumulative_scores = calculate_cumulative_scores(table_values)

    return render_template('scores.html', players=players, form=form, table_cols=table_cols, table_values=cumulative_scores)
