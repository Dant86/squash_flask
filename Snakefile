rule run:
	shell:
		"python app/squash_main.py run"

rule run_dev:
	shell:
		"python app/squash_main.py run_dev"

rule init:
	shell:
		"python app/models.py db init"

rule upgrade:
	shell:
		"python app/models.py db upgrade"

rule migrate:
	shell:
		"python app/models.py db migrate"

rule clear:
	shell:
		"python app/models.py clear"