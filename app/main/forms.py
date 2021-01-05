from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required


class LoginForm(Form):
    """Accepts a room."""
    room = StringField('Game Code', validators=[Required()])
    submit_join = SubmitField('Join Game')
    submit_create = SubmitField('Create a New Game')


class NameForm(Form):
    """Accepts a room."""
    name = StringField('Name', validators=[Required()])
    submit = SubmitField('Set Name')

