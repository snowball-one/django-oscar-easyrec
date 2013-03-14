.PHONY: docs

install:
	python setup.py develop --upgrade
	pip install -r requirements.txt

sandbox: install
	- rm sandbox/sandbox/db.sqlite3
	sandbox/manage.py syncdb --noinput
	sandbox/manage.py migrate
	sandbox/manage.py loaddata sandbox/fixtures/auth.json

test:
	./run_tests.py tests/

travis: install test

docs:
	$(MAKE) -C docs html
