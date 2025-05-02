from django.test import TestCase
from django.urls import reverse

class HomepageTest(TestCase):
    def homepage_status_code(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)