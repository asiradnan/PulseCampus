from django.test import TestCase
from users.models import User, Principal

class PrincipalModelTestCase(TestCase):
    def setUp(self):
        self.principal = Principal.objects.create(
            user=User.objects.create_user(username='principal', password='password'),
            name='John Doe',
            email='john@example.com',
            phone_number='1234567890',
            address='123 Main St',
            date_of_birth='1990-01-01'
        )

    def test_stringify(self):
        self.assertEqual(str(self.principal), 'John Doe')


