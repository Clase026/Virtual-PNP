from flask import session, redirect, url_for, render_template, request
from . import main
import models

SAVE_MESSAGE = "Changes saved successfully!"

@main.route('/signin/', methods=['GET'])
def signin():
    """The first login form"""
    return render_template('index.html',error='')

@main.route('/dosignin', methods=['POST'])
def dosignin():
    """"Action to enter a room from the login page."""
    if request.method == "POST":
        session["name"] = models.db.Player.check_username_password(request.form["inputName"],request.form["inputPassword"])
        if session.get("player") == None:
            return render_template('index.html',error='Incorrect username or password')
        session["room"] = "Test"
        return redirect(url_for('.chat'))

@main.route('/signup/', methods=['GET'])
def signup():
    """The form used to sign up for the service"""
    return render_template('signup.html',error='')

@main.route('/dosignup', methods=['POST'])
def dosignup():
    """Action to sign a user up for virtual P&P"""
    if not models.db.Player.check_username_taken(request.form["inputName"]):
        new_player = models.db.Player(request.form["inputName"],request.form["inputPassword"])
        models.db.session.add(new_player)
        models.db.session.commit()
        return redirect(url_for('.signin',error=''))
    else:
        return redirect(url_for('.signup',error='Username taken'))

@main.route('/')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.signin',error=''))
    return render_template('chat.html', name=name, room=room)

@main.route('/save_changes', methods=['POST'])
def save_attributes():
    """Saves changes that players make to their character's attributes and saving throws"""
    if request.method == "POST":
        character = models.db.Character.get_character_by_username_game(session.get('name'),session.get('room'))
        character.attributes = request.form['Strength'] + '10,10,10,10,10'
        character.attributebonuses = request.form['StrengthBonus'] + '0,0,0,0,0'
        character.savingthrows = request.form['StrengthSave'] + '0,0,0,0,0'
        models.db.session.commit()
        saved = SAVE_MESSAGE
        return render_template('edit_attributes.html', saved=saved)

@main.route('/editattributes/')
def edit_attributes():
    """A form page that lets the player edit their character's saving throws and attributes"""
    character = models.db.Character.get_character_by_username_game(session.get('name'),session.get('room'))
    session['Strength'] = character.get_proficiency('Strength')
    session['StrengthBonus'] = character.get_proficiency_bonus('Strength')
    session['StrengthSave'] = character.get_save_bonuses('Strength')
    return render_template('edit_attributes.html', saved='')