from app.squash_main import db
import os
from os.path import join, dirname
from dotenv import load_dotenv
from sqlalchemy import create_engine

DOTENV_PATH = join(dirname(__file__), '.env')
load_dotenv(DOTENV_PATH)
P_USER = os.environ.get("POSTGRES_USER")
P_PASS = os.environ.get("POSTGRES_PASS")
LINK = "postgresql://{}:{}@localhost/squash_db".format(P_USER, P_PASS)

rule run:
	shell:
		"python -B app/squash_main.py"
