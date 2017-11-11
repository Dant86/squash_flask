from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os
from os.path import join, dirname
from dotenv import load_dotenv
import datetime
import bcrypt
from sqlalchemy.orm import synonym

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
postgres_user = os.environ.get("POSTGRES_USER")
postgres_pass = os.environ.get("POSTGRES_PASS")
conn = "postgresql://{}:{}@localhost/squash_db".format(postgres_user, postgres_pass)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = conn
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)

tournaments = db.Table('tournaments',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('tournament_id'), db.ForeignKey('tournament.id')
)

class Admin(db.Model):
	__tablename__ = "squash_admin"
	id = db.Column('id', db.Integer, primary_key=True)
	u_name = db.Column('username', db.Unicode)
	_pass_w = db.Column('password', db.Unicode)

	def __init__(self, uname, passw):
		self.u_name = uname
		self._pass_w = passw

	@property
	def password(self):
		return bcrypt.hashpw(self._pass_w.encode("utf8"), bcrypt.gensalt())

	@password.setter
	def password(self, new_pass):
		self._pass_w = new_pass

	password = synonym('_pass_w', descriptor=password)

class User(db.Model):
	__tablename__ = "squash_user"
	id = db.Column('id', db.Integer, primary_key=True)
	f_name = db.Column('first_name', db.Unicode)
	l_name = db.Column('last_name', db.Unicode)
	email = db.Column('email', db.Unicode)
	u_name = db.Column('username', db.Unicode)
	_pass_w = db.Column('password', db.Unicode)
	rank = db.Column('rank', db.Integer)
	tournaments = db.relationship('Tournament', secondary='tournaments', backref = db.backref('players', lazy='dynamic'))


	def __init__(self, fname, lname, email, username, password):
		self.f_name = fname
		self.l_name = lname
		self.email = email
		self.u_name = username
		self._pass_w = password

	@property
	def password(self):
		return bcrypt.hashpw(self._pass_w.encode("utf8"), bcrypt.gensalt())

	@password.setter
	def password(self, new_pass):
		self._pass_w = new_pass

	password = synonym('_pass_w', descriptor=password)

	def __str__(self):
		return "{}".format(self.u_name)

class Tournament(db.Model):
	__tablename__ = "squash_tournament"
	id = db.Column('id', db.Integer, primary_key=True)
	opp_school = db.Column('opp_school', db.Unicode)
	location = db.Column('location', db.Unicode)
	date = db.Column('date', db.Unicode)

	def __init__(self, opp_school, location, date):
		self.opp_school = opp_school
		self.location = location
		self.date = date

class Match(db.Model):
	__tablename__ = "squash_match"
	id = db.Column('id', db.Integer, primary_key=True)
	winner = db.Column('winner', db.Unicode)
	loser = db.Column('loser', db.Unicode)
	score1 = db.Column('score1', db.Unicode)
	score2 = db.Column('score2', db.Unicode)
	score3 = db.Column('score3', db.Unicode)
	score4 = db.Column('score4', db.Unicode)
	score5 = db.Column('score5', db.Unicode)

	def __init__(self, winner, loser, score1, score2, score3, score4, score5):
		self.winner = winner
		self.loser = loser
		self.score1 = score1
		self.score2 = score2
		self.score3 = score3
		self.score4 = score4
		self.score5 = score5

if __name__ == "__main__":
	manager.run()
