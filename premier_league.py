# Import necessary packages

from flask import Flask, render_template, flash, request, url_for, redirect, session, json, abort
import psycopg2
from wtforms import Form, BooleanField, TextField, PasswordField, validators, StringField
from passlib.hash import sha256_crypt
from werkzeug import generate_password_hash, check_password_hash
import gc
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update, select, Column
from flask.ext.mail import Mail
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_security.forms import RegisterForm
from flask_login import current_user
from datetime import datetime
from wtforms.validators import Required
from flask.ext.wtf import Form  
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from flask_security.forms import RegisterForm

from wtforms import (
    Form,
    validators,
    TextAreaField,
    IntegerField,
    BooleanField,
    SelectField,
    DateField,
    FloatField,
    StringField,
)
from sqlalchemy.types import (
    Integer, String, Boolean,
    Unicode, DateTime, Float,
    PickleType,
)

print(sys.path)

app = Flask(__name__)

# Update config parameters for the use of the application

# Set the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:bukmacher@localhost/epl'

app.config['SECRET_KEY'] = 'super-secret'

# Enable registering users
app.config['SECURITY_REGISTERABLE'] = True

# Enable confirming registration by email
app.config['SECURITY_CONFIRMABLE'] = False

# Enable recovering passwords
app.config['SECURITY_RECOVERABLE'] = True

# Set passwords hash and salt
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'
app.config['SECURITY_PASSWORD_SALT'] = 'fhasdgihwntlgy8f'

# Enable sending emails to users
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'bet.epl.info@gmail.com',
    MAIL_PASSWORD = 'bukmacher',
))

# Setup mail extension
mail = Mail(app)


app.debug = True
db = SQLAlchemy(app)


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
	stadium = db.Column(db.String(255)))			

class Game_Week:
	__tablename__ = 'game_week'
	match_id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
	team_home_id = db.Column(db.Integer(), db.ForeignKey('teams.team_id'))
	team_away_id = db.Column(db.Integer(), db.ForeignKey('teams.team_id'))
	"1" = db.Column(db.Float())
	"X" = db.Column('X', db.Float())
	"2" = db.Column('2', db.Float())
	score_home = db.Column(db.Integer())
	score_away = db.Column(db.Integer())
	game_week = db.Column(db.Integer())
	match_date = db.Column(db.Date())
	team_home_name = db.Column(db.String(255))
	team_away_name = db.Column(db.String(255)))		

class User_Wallet:
	__tablename__ = 'user_wallet'
	wallet_id = db.Column(db.Integer(),autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
	points_available = db.Column(db.Integer())
	points_won = db.Column(db.Float()))
		
class User_Bets:
	db.Column('bet_id', db.Integer(),autoincrement=True, primary_key=True)
	db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
	db.Column('game_week', db.Integer())
	db.Column('match_id', db.Integer(), db.ForeignKey('game_week.match_id'))
	db.Column('points_won', db.Float())
	db.Column('bet', db.String(1))
	db.Column('points_bet', db.Integer()))
		
class Team_Statistics:
	id = db.Column(db.Integer(), db.ForeignKey('teams.team_id'))
	team_id = db.Column(db.Integer(), db.ForeignKey('teams.team_id'))
	matches = db.Column(db.Integer())
	wins = db.Column(db.Integer())
	loses = db.Column(db.Integer())
	drawn = db.Column(db.Integer())
	points = db.Column(db.Integer())
	"GF" = db.Column(db.Integer())
	"GA" = db.Column(db.Integer())
	"GD" = db.Column(db.Integer()))

#db.create_all()		
	

user_datastore = SQLAlchemyUserDatastore(db, User, Role)


# Exted registration form with username field
class ExtendedRegisterForm(RegisterForm):  

	# Add username field to the register's class
    username = StringField('Nazwa użytkownika', [DataRequired()])

    def validate(self):
		# Add username validation: return: True is the form is valid
        
        # Use standard validator
        validation = Form.validate(self)
        if not validation:
            return False

        # Check if username already exists       
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            # Text displayed to the user
            self.username.errors.append('Username already exists')
            return False

        return True

# Setup Flask-Security
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)		


# Main page

@app.route('/')
def index():
	return render_template('index.html')

	
# Results of matches from last week
# Note: In condition 'game_week = 4', 4 is contemporary value and should be replaced with a variable specifying the number of last game week
	
@app.route('/lastgw')
def lastgw():
    conn=psycopg2.connect("dbname='epl' user='postgres' password='bukmacher' host=localhost port=5432")
    cursor = conn.cursor()
	
	# Select table with matches results for last game week
    cursor.execute("""SELECT match_date, team_home_name, score_home, score_away, team_away_name from game_week where game_week=4""")
    items = cursor.fetchall()
	
    return render_template('lastgw.html', items=items)
	
	
# Results of matches for current week along with their course values
# Note: In condition 'game_week = 5', 5 is contemporary value and should be replaced with a variable specifying the number of current game week
	
@app.route('/bets')
def bets():
    conn=psycopg2.connect("dbname='epl' user='postgres' password='bukmacher' host=localhost port=5432")
    cursor = conn.cursor()

	# Select table with matches results for current game week
    cursor.execute("""SELECT match_date,team_home_name,score_home,score_away, team_away_name,"1","X","2" from game_week where game_week=5""")
    items = cursor.fetchall()
	
    return render_template('bets.html', items=items)


# Ranking of teams

@app.route('/rank_teams')
def rank_teams():
	conn=psycopg2.connect("dbname='epl' user='postgres' password='bukmacher' host=localhost port=5432")
	cursor = conn.cursor()
	
	# Select table with statistics of teams ordering them by number of points
	cursor.execute("""SELECT team_name, matches, wins, loses, drawn, "GF", "GA", "GD", points FROM team_statistics JOIN teams ON team_statistics.team_id = teams.team_id ORDER BY points DESC""")
	items = cursor.fetchall()
	
	items = [[a+1] + list(alist) for a, alist in enumerate(items)]
	
	return render_template('rank_teams.html', items=items)
	
	
# Ranking of users
	
@app.route('/rank_users')
@login_required
def rank_users():
	conn=psycopg2.connect("dbname='epl' user='postgres' password='bukmacher' host=localhost port=5432")
	cursor = conn.cursor()
	
	# Select table with number of points won by the users ordering them descendally by number of points	
	cursor.execute("""SELECT username, points_won FROM "user" INNER JOIN user_wallet ON "user".id = user_wallet.user_id ORDER BY points_won DESC""")
	items = cursor.fetchall()
	
	items = [[a+1] + list(alist) for a, alist in enumerate(items)]
	
	return render_template('rank_users.html', items=items)
	
	
# User profile

@app.route('/profile/<username>', methods=['POST', 'GET'])
@login_required
def profiles(username):

	user = User.query.filter_by(username=current_user.username).first()
	user_id = current_user.get_id()
	conn=psycopg2.connect("dbname='epl' user='postgres' password='bukmacher' host=localhost port=5432")
	cursor = conn.cursor()
	
	# Select number of available points of the user
	cursor.execute("""SELECT points_available, points_won FROM user_wallet where user_id=%s""", user_id)
	wallet_state = cursor.fetchall()
	
	# Select last 10 bets of the user
	cursor.execute("""SELECT  user_bets.game_week, game_week.team_home_name, game_week.team_away_name, user_bets.bet, user_bets.points_bet, user_bets.points_won FROM user_bets JOIN game_week ON game_week.match_id = user_bets.match_id where user_bets.user_id=%s ORDER BY user_bets.match_id DESC LIMIT 10""", user_id)
	last_10_bets = cursor.fetchall()
	
	# Select the position of the user in ranking
	cursor.execute("""SELECT RowNr FROM (SELECT  user_id, ROW_NUMBER() OVER (ORDER BY points_won DESC) AS RowNr, points_won from user_wallet) sub where sub.user_id = %s""", user_id)
	position_of_user = cursor.fetchall()

	return render_template('profile.html', user=user, wallet_state=wallet_state, last_10_bets=last_10_bets, position_of_user=position_of_user)


# Adding a new bet

@app.route('/new_bet', methods=['POST', 'GET'])
@login_required
def new_bet():
	conn=psycopg2.connect("dbname='epl' user='postgres' password='bukmacher' host=localhost port=5432")
	cursor = conn.cursor()
	user_id = current_user.get_id()
	
	#class AddBet(Form):

	#	bet = SelectField(
	#		'bet',
	#		choices=[
	#			(' --- ', ' --- '),
	#			('hosts', 'Gospodarze'),
	#			('guests', 'Goście'),
	#			('drawn', 'Remis'),
	#	]
	#)
		
	#	points = SelectField(
	#		'points',
	#		choices=[
	#			(str(i), i) for i in range(11)
	#	]
	#)
	
	#form = AddBet(request.form)
	
	# Note: 5 is contemporary value and this variable should contain the number of curreent game week
	current_game_week = 5
	
	# Select matches for current week along with their course values
	cursor.execute("""SELECT match_id, match_date,team_home_name,score_home,score_away, team_away_name,"1","X","2" from game_week where game_week=%s""",(current_game_week,))
	matches_table = cursor.fetchall()
	
	# Select number of available points of the user
	cursor.execute("""SELECT points_available FROM user_wallet where user_id=%s""", user_id)
	available_points = cursor.fetchall()

	# Select bets of the user		
	cursor.execute("""SELECT match_id, bet, points_bet from user_bets where user_id=%s and game_week=%s""", (user_id, current_game_week))
	previous_user_bets = cursor.fetchall()
	
	# Gather match_id and bet from bets of the user in order to check later if he's not betting the same match
	previous_bets_matches = []
	previous_bets_bets = []
	
	for i in previous_user_bets:
		previous_bets_matches.append(i[0])
		previous_bets_bets.append(i[1])
	
	# Betting workflow
	if request.method == 'POST':
	
		# How to get results for all rows?
		#bet = form.bet.data
		#print(bet)
	
		from pprint import pprint as pp
		
		# List with submitted user bets
		obstawienia = request.form
		print(request.form)
		
		# Counter for bet points
		points_bet_sum = 0
		
		# List of bets to insert to database
		pass_to_db_list=[]
		
		for i in range(len(matches_table)):
			kto_iterate = 'kto' + '_' + str(i+1)
			ile_iterate = 'ile' + '_' + str(i+1)
			#print(obstawienia[kto_iterate],obstawienia[ile_iterate])
			
			# Check if every selected bet has points assigned and vice versa
			if (obstawienia[kto_iterate] == ' --- ' and obstawienia[ile_iterate] != ' --- ') or (obstawienia[ile_iterate] == ' --- ' and obstawienia[kto_iterate] != ' --- '):
				flash('Wysłane dane są niepełne. Upewnij się, że wybierasz liczbę punktów dla danego obstawienia')
				break
				
				
			else:
			# Gather all bets and count total sum of bet points
				if obstawienia[ile_iterate] != ' --- ':
					points_bet_sum = points_bet_sum + int(obstawienia[ile_iterate])
					
				if obstawienia[kto_iterate] == 'Gospodarze':
					pass_to_db_list.append((current_user.id, current_game_week, matches_table[i][0], 'H', obstawienia[ile_iterate]))
					
				if obstawienia[kto_iterate] == 'Goście':
					pass_to_db_list.append((current_user.id, current_game_week, matches_table[i][0], 'G', obstawienia[ile_iterate]))
					
				if obstawienia[kto_iterate] == 'Remis':
					pass_to_db_list.append((current_user.id, current_game_week, matches_table[i][0], 'D', obstawienia[ile_iterate]))

					
		#print(pass_to_db_list)
		
		
		if points_bet_sum > 0:
		
			# Check if user has enough number of points for bets
			if int(available_points[0][0]) < points_bet_sum:
				flash('Nie posiadasz wystarczającej liczby punktów, by dokonać tej operacji')
				
				
			else:
				for row in pass_to_db_list:
				
				# Check if match and bet does not already exist in previous user bets
					if row[2] in previous_bets_matches and row[3] in previous_bets_bets:					
						
						# If user tries to set the same bet for the same match add points to this bet in database 
						cursor.execute("""UPDATE user_bets SET points_bet = points_bet + %s where match_id = %s and user_id = %s""", (int(row[4]), row[2], user_id))
						conn.commit()
						
						# Otherwise insert the bet into database
					else:
						cursor.executemany("""INSERT INTO user_bets (user_id, game_week, match_id, bet, points_bet) VALUES (%s, %s, %s, %s, %s)""", (row,))
						
				# Subtract the value of available points of the user by sum of bet points	
				new_wallet = available_points[0][0] - points_bet_sum
				wallet_update = (new_wallet, current_user.id)
				
				# Update the number of available points of the user
				cursor.execute("""UPDATE user_wallet SET points_available =%s where user_id =%s""", (wallet_update))
				conn.commit()
				cursor.close()
				
				
				flash('Nowe zakłady zostały dodane')			
			
	matches_table = [[a+1] + list(alist) for a, alist in enumerate(matches_table)]
	
	return render_template('new_bet.html', matches_table=matches_table, available_points=available_points, previous_user_bets=previous_user_bets)
 
if __name__ == "__main__":
    app.run()
