from flask import redirect, render_template, request, session, url_for, flash
from flask_socketio import emit
import uuid
import random

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
            2: [1, 1],
            5: [3, 2],
            6: [4, 2],
            7: [4, 3],
            8: [5, 3],
            9: [6, 3],
            10:[6, 4]
        }
        
        # each quest in order
        # tuple of (number of people, how many needed to fail.)
        self.quest_balance = {
            2 : [(1,1),(1,1),(1,1),(1,1),(1,1)],

            5 : [(2, 1), (3, 1), (2, 1), (3, 1), (3, 1)],
            6 : [(2, 1), (3, 1), (4, 1), (3, 1), (4, 1)],
            7 : [(2, 1), (3, 1), (3, 1), (4, 2), (4, 1)],
            8 : [(3, 1), (4, 1), (4, 1), (5, 2), (5, 1)],
            9 : [(3, 1), (4, 1), (4, 1), (5, 2), (5, 1)],
            10: [(3, 1), (4, 1), (4, 1), (5, 2), (5, 1)],
        }

        # TODO: perhaps also include role description with the role?
        # returns roles in {name: {Name:, Team:, Number:}}
        # self.roles = get_roles("app/games/AvalonGame/avalon_roles.csv")
        self.roles = get_roles()
        self.rules = {
            "Vote Rule": False,
            # "Targetting": False,
            # "Good Can Fail" : False,
            # "Custom Quests": False,
        }

        # game variables that need to be reset each game.
        self.active_roles = []
        self.assigned_roles = {} # user: role

        self.player_order = []
        self.leader = "" # UID

        """
            quests -> a single value() from quest_balance.
            quest_outcomes -> list of nums. 0=not done, 1=Good, -1 = Evil
        """
        self.quest_tracker = {}

        self.vote_tracker = {}


    def setup_game(self, roles):
        self.active_roles = roles
        # Sets up quests tracking.
        self.quest_tracker = {
            "quests" : self.quest_balance[self.player_count],
            "quest_outcomes" : [0, 0, 0, 0, 0], # 1 = GOOD, -1 = EVIL
        }
        # Sets up vote tracking
        self.vote_tracker = {
            'round' : 1,
            1 : [],
            2 : [],
            3 : [],
            4 : [],
            5 : [],
        }


        # Shuffles roles.
        random.shuffle(roles)
        # TODO: perhaps also shuffle player order?
        self.player_order = list(self.players.keys())
        self.assigned_roles = {self.player_order[i]: roles[i] for i in range(len(roles))}

        # Chooses leader
        leader_int = random.randint(0, self.player_count-1)
        self.leader = self.player_order[leader_int]
        # self.vote_tracker[self.vote_tracker['round']].append()

    def game_name(self):
        return "Avalon"


# socketIO events specific to avalon
"""
    message: 
        scene : int. Indicates which scene the player is coming from.
        room: str. The room IDs

    This function transitions from the common lobby (scene 0)
    to the role/rule picking (scene 1)
"""
@socketio.on('Avalon_ready')
def avalon_ready(message):
    room = message["room"]

    game = games_db.get_game(room)
    
    # TODO: Rule selection
    balance = game.team_balance[game.player_count]
    emit('game_planning', {"roles": game.roles, "balance": balance}, room=room)

@socketio.on("v1_select_change")
def v1_select_change(message):
    room = message["room"]
    emit('v1_select_change', message, room=room)

@socketio.on("v1_finish")
def v1_finish(message):
    room = message["room"]
    roles = message['roles']
    
    # assign the roles
    game = games_db.get_game(room)
    game.setup_game(roles)
    games_db.save_game(game)

    # emit the move to view 2
    emit('v2_night', {"assigned_roles" : game.assigned_roles}, room=room)



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