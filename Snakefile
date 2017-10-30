from app.squash_main import db

rule run:
	shell:
		"python -B app/squash_main.py"

rule db_create:

rule db_drop:
	run:
		db.drop()

