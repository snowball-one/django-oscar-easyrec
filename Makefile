.PHONY: docs

install:
	python setup.py develop --upgrade
	pip install -r requirements.txt

sandbox: install
 	[-f sandbox/sandbox/db.sqlite ] && rm sandbox/sandbox/db.sqlite || true
	# Create database
	sandbox/manage.py syncdb --noinput
	sandbox/manage.py migrate
	# Import some fixtures
	sandbox/manage.py oscar_import_catalogue sandbox/fixtures/books-catalogue.csv
	sandbox/manage.py oscar_import_catalogue_images sandbox/fixtures/books-images.tar.gz
	sandbox/manage.py loaddata countries.json
	sandbox/manage.py rebuild_index --noinput

test:
	./run_tests.py tests/

travis: install test

docs:
	$(MAKE) -C docs html
