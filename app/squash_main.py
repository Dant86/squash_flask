from flask import *
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os
from os.path import join, dirname
from dotenv import load_dotenv
import datetime
import bcrypt
import sys
from models import *

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
postgres_user = os.environ.get("POSTGRES_USER")
postgres_pass = os.environ.get("POSTGRES_PASS")
conn = "postgresql://{}:{}@localhost/squash_db".format(postgres_user, postgres_pass)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = conn
app.secret_key = os.environ.get("APP_SECRET_KEY")
db = SQLAlchemy(app)

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
		fname = request.form.get("fname").lower().capitalize()
		lname = request.form.get("lname").lower().capitalize()
		email = request.form.get("email")
		uname = request.form.get("username")
		passw = request.form.get("password")
		passw = bcrypt.hashpw(passw.encode("utf8"), bcrypt.gensalt())
		new_user = User(fname, lname, email, uname, passw)
		db.session.add(new_user)
		db.session.commit()
		session["user"] = new_user.id
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
	users.sort(key=lambda x: x.rank)
	return render_template("roster.html", users=users)

# @app.route()

if __name__ == "__main__":
	args = sys.argv
	if args[1] == "run":
		app.run()
	elif args[1] == "run_dev":
		app.run(debug=True)
