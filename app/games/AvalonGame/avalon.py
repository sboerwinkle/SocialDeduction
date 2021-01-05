from flask import redirect, render_template, request, session, url_for, flash
from flask_socketio import emit
import uuid

from . import avalon_bp
from ... import socketio
from ...main.forms import LoginForm, NameForm
from ..game import Game

"""
    Avalon general planning.
    Views needed:
    1. Planning stage (Choose roles and rules to play with)
    2. Night phase (everyone is assigned a role)
    3. Quest Picking Phase (leader chooses a quest)
    4. Quest Voting Phase (everyone votes on quest)
    5. Quest P/F Phase (people on quest choose to pass or fail)
    6. End of Game Voting Phase for assassin (somtimes)
    7. End of Game Screen.
"""

class Avalon(Game):

    def __init__(self, room_id):
        min_players = 2
        max_players = 10 
        Game.__init__(self, room_id, min_players, max_players)


    def game_name(self):
        return "Avalon"


# socketIO events specific to avalon
@socketio.on('Avalon_start')
def avalon_start(message):
    # role picker and rule picker.
    pass




# game route
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