from project.settings._common import *

DEBUG = True

try:
    INSTALLED_APPS.remove('south')
except:
    pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'