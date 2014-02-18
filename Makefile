.PHONY: docs

install:
	python setup.py develop --upgrade
	pip install -r requirements.txt

sandbox: install
	# Remove previous db file if it exists
	-rm -f sandbox/sandbox/db.sqlite3
	# Create database
	sandbox/manage.py syncdb --noinput
	sandbox/manage.py migrate
	# Import some fixtures
	sandbox/manage.py oscar_import_catalogue sandbox/fixtures/books-catalogue.csv
	sandbox/manage.py oscar_import_catalogue_images sandbox/fixtures/books-images.tar.gz
	sandbox/manage.py loaddata countries.json

test:
	./run_tests.py

travis: install
	./run_tests.py --cover-erase --with-coverage --cover-package=easyrec --cover-html --cover-html-dir=coverage
	coveralls

docs:
	$(MAKE) -C docs html
