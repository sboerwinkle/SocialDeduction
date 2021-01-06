from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio

from ..games import Player, Game, Avalon
from . import games_db


@socketio.on('joined')
def joined(message):
    """Sent by clients when they enter a room"""
    room = message["room"]
    join_room(room)

    # add player to game
    game = games_db.get_game(room)
    game.add_player(session.get("player_id"), session.get("player_name"))
    games_db.save_game(game)
    out_dict = {
        "type": "add",
        "change": {'player': session.get('player_name')},
        "players": game.get_players(is_dict=True)
    }
    # Emit change
    emit('player_change', out_dict, room=room)


@socketio.on('left')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = message["room"]
    player = message["player_name"]

    # remove player from game
    game = games_db.get_game(room)
    game.remove_player(session.get("player_id"), session.get("player_name"))
    games_db.save_game(game)
    leave_room(room)
    out_dict = {
        "type": "leave",
        "change": {'player': player},
        "players": game.get_players(is_dict=True)
    }
    # emit change
    emit('player_change', out_dict, room=room)


@socketio.on('ready_change')
def ready_change(message):
    room = message["room"]
    player_id = message["player_id"]
    ready = message["ready"]

    # first emit ready change
    game = games_db.get_game(room)

    # short circuit to prevent multiple requests

    game.ready_change_player(player_id, ready)
    out_dict = {
        "type": "ready",
        "change": {'player': session.get('player_name'), "ready": ready},
        "players": game.get_players(is_dict=True)
    }
    emit('player_change', out_dict, room=room)

    # we need to check if all players are ready, and we can start the game.
    if ready and game.everyone_ready():
        game.started = True
        game.reset_ready()
        emit('game_start', {}, room=room)
        pass

    games_db.save_game(game)


@socketio.on('text')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = message["room"]
    player = message["player_name"]
    emit('message', {'msg': player + ': ' + message['msg']}, room=room)
