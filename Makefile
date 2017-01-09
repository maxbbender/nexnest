install:
	pip install --upgrade pip
	pip install -r requirements.txt

	make sync

sync:
	# Database Sync

	# nexnest_development ~~ Drop->Create->Version Control->InitDB->[INIT DATA]
	dropdb -U nexnest_development nexnest_development --if-exists
	createdb -U nexnest_development -O nexnest_development -h localhost -p 5432 nexnest_development
	python db/manage.py version_control
	python db/manage.py upgrade

	# nexnest_test ~~ Drop->Create->Version Control->InitDB->[INIT DATA]
	dropdb -U nexnest_test nexnest_test --if-exists
	createdb -U nexnest_test -O nexnest_test -h localhost -p 5432 nexnest_test
	NEXNEST_ENV=test python db/manage.py version_control
	NEXNEST_ENV=test python db/manage.py upgrade

user_setup:
	sudo -u postgres createuser -U postgres -p 5432 -d -w nexnest_development
	sudo -u postgres psql -U postgres -c "alter user nexnest_development with password 'domislove';"

	sudo -u postgres createuser -U postgres -p 5432 -d -w nexnest_test
	sudo -u postgres psql -U postgres -c "alter user nexnest_test with password 'domislove';"

script:
	@read -p "What is the name of the migration :" script_name; \
	python db/manage.py script $$script_name;

upgrade:
	python db/manage.py upgrade

erd:
	eralchemy -i postgres://nexnest_development:domislove@localhost:5432/nexnest_development -o docs/erd.pdf

server:
	python server.py