from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm
from logging import StreamHandler

SAVE_MESSAGE = "Changes saved successfully!"

@main.route('/signin/', methods=['GET'])
def signin():
    """The login form to enter a room"""
    return render_template('index.html')

@main.route('/dosignin', methods=['POST'])
def dosignin():
    """"Action to enter a room from the login page."""
    if request.method == "POST":
        session["name"] = request.form['inputName']
        session["room"] = request.form['inputRoom']
        return redirect(url_for('.chat'))
    #form = LoginForm()
    #if form.validate_on_submit():
        #session['name'] = form.name.data
        #session['room'] = form.room.data
        #return redirect(url_for('.chat'))
    #elif request.method == 'GET':
        #form.name.data = session.get('name', '')
        #form.room.data = session.get('room', '')

    #return render_template('index.html', form=form)

@main.route('/')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.signin'))
    return render_template('chat.html', name=name, room=room)

@main.route('/save_changes', methods=['POST'])
def save_attributes():
    """Saves changes that players make to their character's attributes and saving throws"""
    if request.method == "POST":
        session['strength'] = request.form['strength']
        saved = SAVE_MESSAGE
        return render_template('edit_attributes.html', saved=saved)

@main.route('/editattributes/')
def edit_attributes():
    """A form page that lets the player edit their character's saving throws and attributes"""
    return render_template('edit_attributes.html', saved='')