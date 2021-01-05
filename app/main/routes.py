import sys
import os
import pickle
import redis
import string
import random
import uuid
from flask import redirect, render_template, request, session, url_for, flash
from flask_socketio import emit

from . import main
from .forms import LoginForm, NameForm
from ..games import Player, Avalon

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
            if get_game(form.room.data) is None:
                print("Room not found.", flush=True)
                # TODO: Visually tell user room was not found.
            else:
                return redirect(url_for('.game_room', game_name=game_name, room_id=session['room']))
        # create new game
        else:
            # generates new ID
            session['room'] = generate_room_id()
            while(get_game(session['room']) is not None):
                session['room'] = generate_room_id()
            game = eval(inv_games_dict[game_name])(session['room'])
            save_game(game)
            return redirect(url_for('.game_room', game_name=game_name, room_id=session['room']))
            

    # GET: first time on webpage.
    elif request.method == 'GET':
        form.room.data = session.get('room', '')

    return render_template("game_login.html", form=form, game=game_name)


@main.route('/game/<game_name>/<room_id>',  methods=['GET', 'POST'])
def game_room(game_name, room_id):
    if "player_id" not in session:
        session['player_id'] = str(uuid.uuid4())
    
    if "player_name" not in session:
        form = NameForm()
        if form.validate_on_submit():
            session['player_name'] = form.name.data
        elif request.method == 'GET':
            return render_template("name.html", form=form)
    
    html_file = "games/"+game_name+".html"
    # return render_template(html_file, room_id=room_id)
    return render_template(html_file, room_id=room_id, player_id=session["player_id"], player_name=session["player_name"])


def generate_room_id():
    """Generate a random room ID"""
    id_length = 5
    return ''.join(random.SystemRandom().choice(
        string.ascii_uppercase) for _ in range(id_length))


# redis database stuff
db = redis.Redis("localhost")
REDIS_TTL_S = 60*10 if os.environ.get('FLASK_DEV', False) else 60*60*12


def get_game(room_id):
    gm = db.get(room_id)
    if gm:
        return pickle.loads(gm)
    else:
        return None


def save_game(game):
    db.setex(game.room_id, REDIS_TTL_S, pickle.dumps(game))
