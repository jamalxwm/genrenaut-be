import os
import pytest
import django
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'genrenaut.settings.local'

def pytest_configure():
    settings.DEBUG = False
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
    django.setup()

@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }

@pytest.fixture
def db(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        yield