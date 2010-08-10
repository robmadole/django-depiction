import unittest
import types
import os

from django.conf import settings

from depiction.decorator import kgrind


class TestDecorator(unittest.TestCase):
    def setUp(self):
        settings.PROFILING = True

    def test_decorator_returns_function(self):
        @kgrind('test.kgrind')
        def specimen(*args, **kwargs):
            print 'Hello'
            return True

        self.assertTrue(type(specimen) == types.FunctionType)

    def test_creates_kgrind_file(self):
        @kgrind('test.kgrind')
        def specimen(*args, **kwargs):
            print 'Hello'

        specimen()

        self.assertTrue('test.kgrind' in os.listdir('.'))
        os.unlink('test.kgrind')
