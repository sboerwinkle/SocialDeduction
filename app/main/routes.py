import sys
import os
import string
import random
import uuid
from flask import redirect, render_template, request, session, url_for, flash
from flask_socketio import emit

from . import main, games_db
from .forms import LoginForm, NameForm
from ..games import Player, Game
from ..games import Avalon, avalon_bp as avalon

# Key: name, value: URL-base
games_dict = {
    "Avalon": "avalon",
    "Werewords": "werewords",
}
inv_games_dict = {v: k for k, v in games_dict.items()}


@main.route('/', methods=['GET', 'POST'])
def index():
    # Game is chosen, process button press
    if request.method == 'POST':
        selected_game = [x for x in games_dict.keys() if x in request.form][0]
        return redirect(url_for('.game_home', game_name=games_dict[selected_game]))

    # Just get the webpage for list of games
    return render_template("index.html", games_list=games_dict.keys())


@main.route('/game/<game_name>/', methods=['GET', 'POST'])
def game_home(game_name):
    game_name = game_name.lower()
    # form submission, joiining a game or creating a new one
    form = LoginForm()
    if form.validate_on_submit():
        # join existing
        if form.submit_join.data:
            session['room'] = form.room.data
            if games_db.get_game(form.room.data) is None:
                print("######### Room not found.", flush=True)
                # TODO: Visually tell user room was not found.
            else:
                game = games_db.get_game(form.room.data)
                if game.player_count >= game.max_players:
                    print("######### Room is full.")
                    # TODO: Visual cue that room is full
                elif game.started:
                    print("######### Room has already started game.")
                    # TODO: Visual cue that game is started
                else:
                    # join game.
                    return redirect(url_for(game_name+'.game_room', room_id=session['room']))
        # create new game
        else:
            # generates new ID
            session['room'] = generate_room_id()
            while(games_db.get_game(session['room']) is not None):
                session['room'] = generate_room_id()
            
            # call constructor
            game = eval(inv_games_dict[game_name])(session['room'])
            games_db.save_game(game)
            return redirect(url_for(game_name+'.game_room', room_id=session['room']))
            

    # GET: first time on webpage.
    elif request.method == 'GET':
        form.room.data = session.get('room', '')

    return render_template("game_login.html", form=form, game=game_name)


def generate_room_id():
    """Generate a random room ID"""
    id_length = 5
    return ''.join(random.SystemRandom().choice(
        string.ascii_uppercase) for _ in range(id_length))