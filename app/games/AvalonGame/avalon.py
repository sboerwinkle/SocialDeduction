from flask import redirect, render_template, request, session, url_for, flash
from flask_socketio import emit
import uuid

from . import avalon_bp
from ... import socketio
from ...main.forms import LoginForm, NameForm
from ..game import Game

class Avalon(Game):

    def __init__(self, room_id):
        Game.__init__(self, room_id)


    def game_name(self):
        return "Avalon"


from flask import session

@avalon_bp.route('/game/avalon/<room_id>',  methods=['GET', 'POST'])
def game_room(room_id):
    if "player_id" not in session:
        session['player_id'] = str(uuid.uuid4())
    
    if "player_name" not in session:
        form = NameForm()
        if form.validate_on_submit():
            session['player_name'] = form.name.data
        elif request.method == 'GET':
            return render_template("name.html", form=form)
    
    game_info = {}
    game_info["room_id"] = room_id
    game_info["game_name"] = "Avalon"
    game_info["player_id"] = session['player_id']
    game_info["player_name"] = session['player_name']
    
    return render_template("avalon.html", game_info=game_info)
