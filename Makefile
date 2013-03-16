.PHONY: docs

install:
	python setup.py develop --upgrade
	pip install -r requirements.txt

sandbox: install
	-rm -f sandbox/sandbox/db.sqlite3
	# Create database
	sandbox/sandbox/manage.py syncdb --noinput
	sandbox/sandbox/manage.py migrate
	# Import some fixtures
	sandbox/sandbox/manage.py oscar_import_catalogue sandbox/fixtures/books-catalogue.csv
	sandbox/sandbox/manage.py oscar_import_catalogue_images sandbox/fixtures/books-images.tar.gz
	sandbox/sandbox/manage.py loaddata countries.json

test:
	./run_tests.py tests/

travis: install test

docs:
	$(MAKE) -C docs html
