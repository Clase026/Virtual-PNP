# -*- encoding: utf-8 -*-
# begin

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import deferred
from chat import app
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

db.drop_all(app=app)

class Game (db.Model):
    __tablename__ = "Game"
    name = db.Column('Name', db.Unicode)
    gameid = db.Column('GameID', db.Integer, primary_key=True)
    sessionname = db.Column('SessionName', db.Unicode)
    gamecode = db.Column('GameCode', db.Unicode)
    messagelog = deferred(db.Column('MessageLog', db.Text))
    gmnotes = deferred(db.Column('GMNotes', db.Text))

    def __init__(self, name, gamecode):
        self.name = name
        self.gamecode = gamecode
        self.sessionname = "First Session"
        self.messagelog = ""
        self.gmnotes = ""

    def set_message_log(self, message):
        num_messages = self.messagelog.count('<p')
        self.messagelog = self.messagelog + message
        if num_messages > 30:
            first_message_end = self.messagelog.find('p>') + 2
            self.messagelog = self.messagelog[first_message_end:]
        db.session.commit()

class Player (db.Model):
    __tablename__ = "Player"
    username = db.Column('UserName', db.Unicode, primary_key=True)
    pwhash = db.Column('PWHash', db.Unicode)

    def __init__(self,username,password):
        self.username = username
        self.pwhash = generate_password_hash(password)

    def get_player_by_username(self,search_name):
        player = db.session.query(self).filter_by(self.username == search_name).first()
        return player

    def check_username_taken(self,new_username):
        if db.session.query(self).filter_by(self.username == new_username).first():
            return True
        else:
            return False

    def check_username_password(self,username,password):
        login_player = db.session.query(Player).filter_by(self.username == username).first()
        if check_password_hash(login_player.pwhash,password):
            return login_player.username
        else:
            return None


class Character (db.Model):
    __tablename__ = "Character"
    charid = db.Column('CharID', db.Integer, primary_key=True)
    role = db.Column('Role', db.Unicode)
    notes = deferred(db.Column('Notes', db.Text))
    # Unknown SQL type: 'int[6]' 
    attributes = db.Column('Attributes', db.Unicode)
    # Unknown SQL type: 'int[6]' 
    attributebonuses = db.Column('AttributeBonuses', db.Unicode)
    # Unknown SQL type: 'int[6]' 
    savingthrows = db.Column('SavingThrows', db.Unicode)
    proficiencies = db.Column('Proficiencies', db.Unicode)
    maxhp = db.Column('MaxHP', db.Integer)
    currenthp = db.Column('CurrentHP', db.Integer)
    ac = db.Column('AC', db.Integer)
    gear = db.Column('Gear', db.Unicode)
    description = db.Column('Description', db.Unicode)
    ideal = db.Column('Ideal', db.Unicode)
    bond = db.Column('Bond', db.Unicode)
    flaw = db.Column('Flaw', db.Unicode)
    # Unknown SQL type: 'int[9]' 
    spelllevels = db.Column('SpellLevels', db.String)
    game_gameid = db.Column('Game_GameID', db.Integer, db.ForeignKey('Game.GameID'))
    player_username = db.Column('Player_UserName', db.Unicode, db.ForeignKey('Player.UserName'))
    trait = db.Column('Trait', db.Unicode)

    game = db.relationship('Game', foreign_keys=game_gameid)
    player = db.relationship('Player', foreign_keys=player_username)

    def __init__(self,role,game_gameid,player_username):
        self.role = role
        self.game_gameid = game_gameid
        self.player_username = player_username
        self.notes = ''
        self.attributes = '10,10,10,10,10,10'
        self.attributebonuses = '0,0,0,0,0,0'
        self.savingthrows = '0,0,0,0,0,0'
        self.proficiencies = 'Perception: 2, Stealth: 2'
        self.maxhp = 10
        self.currenthp = 10
        self.ac = 10
        self.gear = ''
        self.description = ''
        self.ideal = ''
        self.bond = ''
        self.flaw = ''
        self.spelllevels = '0,0,0,0,0,0,0,0,0'
        self.trait = ''

    def get_character_by_username_game(self,username,game_id):
        character = db.session.query(self).filter_by(self.player_username == username, self.game_gameid == game_id).first()
        return character

    def get_attribute(self,attribute_name):
        cs_attributes = self.attributes.split(',')
        if attribute_name == "Strength":
            return cs_attributes[0]
        if attribute_name == "Dexterity":
            return cs_attributes[1]
        if attribute_name == "Constitution":
            return cs_attributes[2]
        if attribute_name == "Intelligence":
            return cs_attributes[3]
        if attribute_name == "Wisdom":
            return cs_attributes[4]
        if attribute_name == "Charisma":
            return cs_attributes[5]
        return None

    def get_attribute_bonus(self,bonus_name):
        cs_bonuses = self.attributebonuses.split(',')
        if bonus_name == "Strength":
            return cs_bonuses[0]
        if bonus_name == "Dexterity":
            return cs_bonuses[1]
        if bonus_name == "Constitution":
            return cs_bonuses[2]
        if bonus_name == "Intelligence":
            return cs_bonuses[3]
        if bonus_name == "Wisdom":
            return cs_bonuses[4]
        if bonus_name == "Charisma":
            return cs_bonuses[5]
        return None


    def get_save_bonuses(self,bonus_name):
        save_bonuses = self.savingthrows.split(',')
        if bonus_name == "Strength":
            return save_bonuses[0]
        if bonus_name == "Dexterity":
            return save_bonuses[1]
        if bonus_name == "Constitution":
            return save_bonuses[2]
        if bonus_name == "Intelligence":
            return save_bonuses[3]
        if bonus_name == "Wisdom":
            return save_bonuses[4]
        if bonus_name == "Charisma":
            return save_bonuses[5]
        return None

    def get_proficiency_bonus(self,proficiency_name):
        if proficiency_name not in self.proficiencies:
            return None
        proficiencies = self.proficienciessplit(',')
        for proficiency in proficiencies:
            if proficiency_name in proficiency:
                return proficiency.split(':')[1]

class Actions (db.Model):
    __tablename__ = "Actions"
    actionid = db.Column('ActionID', db.Integer, primary_key=True)
    actionname = db.Column('ActionName', db.Unicode)
    actionstring = db.Column('ActionString', db.Unicode)
    isuniversal = db.Column('IsUniversal', db.Boolean)

    def __init__(self,actionstring,isuniversal):
        self.actionstring = actionstring
        self.isuniversal = isuniversal

class Characteractions (db.Model):
    __tablename__ = "CharacterActions"
    character_charid = db.Column('Character_CharID', db.Integer, db.ForeignKey('Character.CharID'),primary_key=True)
    actions_actionid = db.Column('Actions_ActionID', db.Integer, db.ForeignKey('Actions.ActionID'),primary_key=True)

    character = db.relationship('Character', foreign_keys=character_charid)
    actions = db.relationship('Actions', foreign_keys=actions_actionid)

# end
