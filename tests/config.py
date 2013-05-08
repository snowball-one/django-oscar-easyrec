import os

from django.conf import settings, global_settings
from oscar.defaults import OSCAR_SETTINGS
from oscar import OSCAR_CORE_APPS

if not settings.configured:
    # Helper function to extract absolute path
    location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), x)
    settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.sites',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'django.contrib.admin',
            ] + OSCAR_CORE_APPS + [
                'easyrec',
            ],
            TEMPLATE_CONTEXT_PROCESSORS=(
                "django.contrib.auth.context_processors.auth",
                "django.core.context_processors.request",
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.contrib.messages.context_processors.messages",
            ),
            TEMPLATE_DIRS=(
                location('templates'),
            ),
            MIDDLEWARE_CLASSES=global_settings.MIDDLEWARE_CLASSES,
            AUTHENTICATION_BACKENDS=(
                'django.contrib.auth.backends.ModelBackend',
            ),
            ROOT_URLCONF='tests.urls',
            DEBUG=False,
            SITE_ID=1,
            APPEND_SLASH=True,
            HAYSTACK_CONNECTIONS={
                'default': {
                    'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
                },
            },
            EASYREC_ENDPOINT = "http://easyrec-test.com/",
            EASYREC_API_KEY = "apikey",
            EASYREC_TENANT_ID = "tenantid",
             **OSCAR_SETTINGS
        )

