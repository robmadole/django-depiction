from django.core.management import setup_environ

from depiction.tests.fixtures.djangoproject import settings

setup_environ(settings)
