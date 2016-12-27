from app import db
from sqlalchemy import update, select, Column
from datetime import datetime
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin

from sqlalchemy.types import (
    Integer, String, Boolean,
    Unicode, DateTime, Float,
    PickleType,
)

import psycopg2

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
	__tablename__ = 'role'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80), unique=True)
	description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
							
			#__init__(self, name, email):??? shall I perform that??
			#	self.name;
			#	self.email
			
class Teams(db.Model):
	__tablename__ = 'teams'
	team_id = db.Column(db.Integer(), primary_key=True)
	team_name = db.Column(db.String(255))
	stadium = db.Column(db.String(255))

class Game_Week(db.Model):
	__tablename__ = 'game_week'
	match_id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
	team_home_id = db.Column(db.Integer(), db.ForeignKey('teams.team_id'))
	team_away_id = db.Column(db.Integer(), db.ForeignKey('teams.team_id'))
	one = db.Column(db.Float())
	drawn = db.Column(db.Float())
	two = db.Column(db.Float())
	score_home = db.Column(db.Integer())
	score_away = db.Column(db.Integer())
	game_week = db.Column(db.Integer())
	match_date = db.Column(db.Date())
	team_home_name = db.Column(db.String(255))
	team_away_name = db.Column(db.String(255))

class User_Wallet(db.Model):
	__tablename__ = 'user_wallet'
	wallet_id = db.Column(db.Integer(),autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
	points_available = db.Column(db.Integer())
	points_won = db.Column(db.Float())

class User_Bets(db.Model):
	__tablename__ = 'user_bets'
	bet_id = db.Column(db.Integer(),autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
	game_week = db.Column(db.Integer())
	match_id = db.Column(db.Integer(), db.ForeignKey('game_week.match_id'))
	points_won = db.Column(db.Float())
	bet = db.Column(db.String(1))
	points_bet = db.Column(db.Integer())

class Team_Statistics(db.Model):
	__tablename__ = 'team_statistics'
	id = db.Column(db.Integer(),autoincrement=True, primary_key=True)
	team_id = db.Column(db.Integer(), db.ForeignKey('teams.team_id'))
	matches = db.Column(db.Integer())
	wins = db.Column(db.Integer())
	loses = db.Column(db.Integer())
	drawn = db.Column(db.Integer())
	points = db.Column(db.Integer())
	gf = db.Column(db.Integer())
	ga = db.Column(db.Integer())
	gd = db.Column(db.Integer())

