from django.test import TestCase
from users.models import User, Principal

class PrincipalModelTestCase(TestCase):
    def setUp(self):
        self.principal = Principal.objects.create(
            user=User.objects.create_user(
                username='principal',
                password='password',
                first_name = 'John',
                last_name = 'Doe'
            ),
            address='123 Main St',
            room_number='2',
            building_number = '3',
            joining_date = '2025-02-03',
            designation = 'Principal'
        )

    def test_stringify(self):
        self.assertEqual(str(self.principal), 'John Doe')


