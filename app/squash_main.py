from flask import *
from flask.ext.session import Session
import sqlite3
from flask_sqlalchemy import SQLAlchemy, or_
import os
from os.path import join, dirname
from dotenv import load_dotenv
import datetime
import bcrypt

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
postgres_user = os.environ.get("POSTGRES_USER")
postgres_pass = os.environ.get("POSTGRES_PASS")
conn = "postgresql://{}:{}@localhost/squash_db".format(postgres_user, postgres_pass)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = conn
db = SQLAlchemy(app)

sess = Session()
sess.init(app)

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
	u_name = db.Column('username', db.Unicode)
	pass_w = db.Column('password', db.Unicode)
	rank = db.Column('rank', db.Integer, primary_key=True)

	def __init__(self, username, password):
		self.u_name = username
		self.pass_w = password

	def __str__(self):
		return "{} {}".format(self.u_name, self.pass_w)

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

@app.route("/")
def main_ting():
	return redirect("/home")

@app.route("/home")
def homepage():
	return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def prompt_login():
	if request.method == "GET":
		return render_template("login.html")
	if request.method == "POST":
		uname = request.form.get("username")
		passw = request.form.get("password")
		user = User.query.filter(User.u_name.like())


@app.route("/signup", methods=["GET", "POST"])
def show_signup_page():
	if request.method == "GET":
		return render_template("signup.html")
	if request.method == "POST":
		uname = request.form.get("username")
		passw = request.form.get("password")
		passw = bcrypt.hashpw(passw, bcrypt.gensalt())
		new_user = User(uname, passw)
		db.session.add(new_user)
		db.session.commit()
		sess["user"] = new_user
		return redirect("/roster")

@app.route("/matches", methods=["GET", "POST"])
def matches():
	if request.method == "GET":
		all_matches = Match.query.all()
		return render_template("matches.html", matches=all_matches)
	if request.method == "POST":
		winner = request.form.get("winner")
		loser = request.form.get("loser")
		game1 = request.form.get("game1")
		game2 = request.form.get("game2")
		game3 = request.form.get("game3")
		game4 = request.form.get("game4")
		game5 = request.form.get("game5")
		new_match = Match(winner, loser, game1, game2, game3, game4, game5)
		winner = User.query.filter(or_(User.f_name.like(winner[:winner.index(" ")]),
			User.l_name.like(winner[winner.index(" ")+1:])))[0]
		loser = User.query.filter(or_(User.f_name.like(loser[:loser.index(" ")]),
			User.l_name.like(loser[loser.index(" ")+1:])))[0]
		db.session.add(new_match)
		db.session.commit()
		return redirect("/matches")

@app.route("/roster", methods=["GET"])
def show_roster():
	users = User.query.all()
	users.sort(ley=lambda x: x.rank)
	return render_template("roster.html", users=users)

@app.route()

if __name__ == "__main__":
	app.run(debug=True)
