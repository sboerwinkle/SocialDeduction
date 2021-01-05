from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio

from ..games import Player, Avalon
from . import games_db


@socketio.on('joined')
def joined(message):
    """Sent by clients when they enter a room"""
    room = session.get('room')
    join_room(room)

    game = games_db.get_game(room)

    # emit change in game state to javascript as well.


    """A status message is broadcast to all people in the room."""
    emit('status', {'msg': session.get('player_name') + ' has entered the room.'}, room=room)


@socketio.on('text')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('player_name') + ':' + message['msg']}, room=room)


@socketio.on('left')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('player_name') + ' has left the room.'}, room=room)