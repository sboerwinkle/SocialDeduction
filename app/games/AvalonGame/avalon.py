from flask import redirect, render_template, request, session, url_for, flash
from flask_socketio import emit
import uuid

from . import avalon_bp
from .avalon_roles import get_roles
from ... import socketio
from ...main.forms import LoginForm, NameForm
from ...main import games_db
from ..game import Game

"""
    Avalon general planning.
    Views needed:
        0. Lobby (shared between all games)
        1. Planning stage (Choose roles and rules to play with)
        2. Night phase (everyone is assigned a role)
        3. Quest Picking Phase (leader chooses a quest)
        4. Quest Voting Phase (everyone votes on quest)
        5. Quest P/F Phase (people on quest choose to pass or fail)
        6. End of Game Voting Phase for assassin (somtimes)
        7. End of Game Screen.


    Roles have this info:
        Name
        Team (evil/good)
        Number (ie number available)
        Knowledge -> what other roles can they see.
"""


class Avalon(Game):

    def __init__(self, room_id):
        min_players = 2 # currently at 2 just for testing. Real min is 5
        max_players = 10 
        Game.__init__(self, room_id, min_players, max_players)

        # balance of good,bad for <key> num players
        self.team_balance = {
            5: [3, 2],
            6: [4, 2],
            7: [4, 3],
            8: [5, 3],
            9: [6, 3],
            10:[6, 4]
        }

        self.roles = get_roles("app/games/AvalonGame/avalon_roles.csv")
        self.rules = {
            "Vote Rule": False,
            "Targetting": False,
        }
        



    def game_name(self):
        return "Avalon"


# socketIO events specific to avalon
"""
    message: 
        scene : int. Indicates which scene the player is coming from.
        room: str. The room ID

    This function transitions from the common lobby (scene 0)
    to the role/rule picking (scene 1)
"""
@socketio.on('Avalon_ready')
def avalon_ready(message):
    room = message["room"]

    # move
    game = games_db.get_game(room)
    
    # TODO: Rule selection
    emit('game_planning', {"roles": game.roles.values()}, room=room)

    
    
    




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