#!/usr/bin/env python
import sys
from coverage import coverage
from optparse import OptionParser

from django.conf import settings


if not settings.configured:
    datacash_settings = {}
    try:
        from integration import *
    except ImportError:
        datacash_settings.update({
            'EASYREC_HOST': 'testserver.datacash.com',
            'EASYREC_TENENT_ID': 'id',
            'EASYREC_API_KEY': 'key',
        })
    else:
        for key, value in locals().items():
            if key.startswith('EASYREC'):
                datacash_settings[key] = value
                
    settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    }
                },
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.admin',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.sites',
                'easyrec',
                ],
            DEBUG=False,
            SITE_ID=1,
            **datacash_settings
        )

# Needs to be here to avoid missing SETTINGS env var
from django_nose import NoseTestSuiteRunner


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=2)

    c = coverage(source=['easyrec'], omit=['*tests*',])
    c.start()
    num_failures = test_runner.run_tests(test_args)
    c.stop()

    if num_failures > 0:
        sys.exit(num_failures)
    print "Generating HTML coverage report"
    c.html_report()


def generate_migration():
    from south.management.commands.schemamigration import Command
    com = Command()
    com.handle(app='easyrec', initial=True)


if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    run_tests(*args)
