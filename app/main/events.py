from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio


@socketio.on('join')
def join(data):
    """Join a Game Lobby"""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)