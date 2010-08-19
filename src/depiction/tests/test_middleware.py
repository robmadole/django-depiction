from BeautifulSoup import BeautifulSoup
from django.conf import settings
from django.test import TestCase

class RegressionTests(TestCase):
    def setUp(self):
        settings.PROFILING = True

    def test_for_default_profile(self):
        response = self.client.get('/test/middleware', {'prof': ''})

        self.assertEquals(response.status_code, 200)

        soup = BeautifulSoup(response.content)
        trs = soup.findAll('tr', 'main')

        self.assertEquals(len(trs), 7)

        source_filename = trs[6].find('td').contents[1].string

        self.assertTrue('djangoproject/views.py' in source_filename)

    def test_for_filtered_profile(self):
        response = self.client.get('/test/middleware', {'prof': 'views.py'})

        self.assertEquals(response.status_code, 200)

        soup = BeautifulSoup(response.content)
        trs = soup.findAll('tr', 'main')

        # We should only have one line because of the filter
        self.assertEquals(len(trs), 1)

        source_filename = trs[0].find('td').contents[1].string

        # This filter should only contain the views.py
        self.assertTrue('djangoproject/views.py' in source_filename)

    def test_for_pulling_grind_data(self):
        response = self.client.get('/test/middleware', {
            'prof': '', 'grind': ''})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response['Content-Type'],
            'application/kcachegrind')
        self.assertEquals(response['Content-Disposition'],
            'attachment; filename=results.kgrind')
        self.assertTrue('fi=' in response.content)

    def test_for_404(self):
        response = self.client.get('/middleware', {'prof': ''})

        self.assertEquals(response.status_code, 404)

    def test_profiling_turned_off(self):
        settings.PROFILING = False

        response = self.client.get('/test/middleware', {
            'prof': '', 'grind': ''})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, 'You ran a test.')
