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
        "type" : "add",
        "change": {'player': session.get('player_name')},
        "players": game.get_players(is_dict=True)
    }

    """A status message is broadcast to all people in the room."""
    emit('player_change', out_dict, room=room)


@socketio.on('text')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = message["room"]
    player = message["player_name"]
    emit('message', {'msg': player + ':' + message['msg']}, room=room)


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
        "type" : "leave",
        "change": {'player': session.get('player_name')},
        "players": game.get_players(is_dict=True)
    }
    
    emit('player_change', out_dict, room=room)