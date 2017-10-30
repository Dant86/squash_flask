from flask import *
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import os
from os.path import join, dirname
from dotenv import load_dotenv
import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
postgres_user = os.environ.get("POSTGRES_USER")
postgres_pass = os.environ.get("POSTGRES_PASS")
conn = "postgresql://{}:{}@localhost/squash_db".format(postgres_user, postgres_pass)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = conn
db = SQLAlchemy(app)

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
	rank = db.Column('rank', db.Integer)

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

@app.route("/")
def main_ting():
	return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def prompt_login():
	if request.method == "GET":
		return render_template("login.html")
	if request.method == "POST":
		uname = request.form.get("username")
		passw = request.form.get("password")

@app.route("/signup", methods=["GET", "POST"])
def show_signup_page():
	if request.method == "GET":
		return render_template("signup.html")
	if request.method == "POST":
		uname = request.form.get("username")
		passw = request.form.get("password")
		new_user = User(uname, passw)
		db.session.add(new_user)
		db.session.commit()
		return redirect("/roster")

@app.route("/roster", methods=["GET"])
def show_roster():
	users = User.query.all()
	return render_template("roster.html", users=users)

if __name__ == "__main__":
	app.run(debug=True)