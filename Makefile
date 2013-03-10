.PHONY: docs

install:
	python setup.py develop
	pip install -r requirements.txt

sandbox: install
	- rm sandbox/sandbox/db.sqlite3
	sandbox/manage.py syncdb --noinput
	sandbox/manage.py migrate
	sandbox/manage.py loaddata sandbox/fixtures/auth.json

docs:
	$(MAKE) -C docs html
