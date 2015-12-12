from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField, Field
from wtforms.validators import Required

class LoginForm(Form):
    """Accepts a nickname and a room."""
    name = StringField('Name',id="Name",validators=[Required()])
    room = StringField('Room',id="Room",validators=[Required()])
    submit = SubmitField('Enter Chatroom')
