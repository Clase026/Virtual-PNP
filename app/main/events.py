from flask import session
from flask.ext.socketio import emit, join_room, leave_room
from .. import socketio
from . import pnpparser
from models import db

@socketio.on('joined')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    output = pnpparser.nice_parse_input(message['msg'])
    db.Game.set_message_log(output)
    emit('message', {'msg': session.get('name') + ': ' + output}, room=room)


@socketio.on('disconnect')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

