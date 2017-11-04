from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os
from os.path import join, dirname
from dotenv import load_dotenv
import datetime

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

class Admin(db.Model):
	__tablename__ = "squash_admin"
	id = db.Column('id', db.Integer, primary_key=True)
	u_name = db.Column('username', db.Unicode)
	pass_w = db.Column('password', db.Unicode)

class User(db.Model):
	__tablename__ = "squash_user"
	id = db.Column('id', db.Integer, primary_key=True)
	f_name = db.Column('first_name', db.Unicode)
	l_name = db.Column('last_name', db.Unicode)
	email = db.Column('email', db.Unicode)
	u_name = db.Column('username', db.Unicode)
	pass_w = db.Column('password', db.Unicode)
	rank = db.Column('rank', db.Integer)

	def __init__(self, fname, lname, email, username, password):
		self.f_name = fname
		self.l_name = lname
		self.email = email
		self.u_name = username
		self.pass_w = password
		self.rank = self.id

	def __str__(self):
		return "{}".format(self.u_name)

class Tournament(db.Model):
	__tablename__ = "squash_tournament"
	id = db.Column('id', db.Integer, primary_key=True)
	opp_school = db.Column('opp_school', db.Unicode)
	location = db.Column('location', db.Unicode)
	date = db.Column('date', db.DateTime, default=datetime.datetime.utcnow())
	result = db.Column('result', db.Unicode)

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