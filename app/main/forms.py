from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField, Field
from wtforms.validators import Required

class LoginForm(Form):
    """Accepts a nickname and a room."""
    name = Field('Name',id="Name")
    room = Field('Room',id="Room")
    submit = SubmitField('Enter Chatroom')
