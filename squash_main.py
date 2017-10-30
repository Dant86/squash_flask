from flask import *
import sqlite3
from flask_sqlalchemy import  SQLAlchemy
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
postgres_user = os.environ.get("POSTGRES_USER")
postgres_pass = os.environ.get("POSTGRES_PASS")
conn = "postgresql://{}:{}@localhost/squash_db".format(postgres_user, postgres_pass)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = conn
db = SQLAlchemy(app)

class Admin(db.Model):
	__tablename__ == "squash_admin"
	id = db.Column('id', db.Integer, primary_key=True)
	u_name = db.Column('data', db.Unicode)
	pass_w = db.Column('data', db.Unicode)

class User(db.Model):
	__tablename__ == "squash_user"
	id = db.Column('id', db.Integer, primary_key=True)
	u_name = db.Column('data', db.Unicode)
	pass_w = db.Column('data', db.Unicode)
	rank = db.Column('rank', db.Integer)

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
		return (request.form.get("password"))

if __name__ == "__main__":
	app.run()