from django.test import TestCase
from django.contrib.auth.models import User
from .models import Principal
from django.utils import timezone
class PrincipalModelTest(TestCase):
    def test_principal_creation(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        principal = Principal(
            user = user, designation='Principal',
            joining_date=timezone.now().date(),
            address='123 Main St',
            room_number='1010',
            building_number='2020'
        )
        self.assertEqual(principal.user, user)
        self.assertEqual(principal.designation, 'Principal')
        self.assertEqual(principal.joining_date, timezone.now().date())
        self.assertEqual(principal.address, '123 Main St')
        self.assertEqual(principal.room_number, '1010')
        self.assertEqual(principal.building_number, '2020')
        self.assertEqual(principal.user.username, 'testuser')
        self.assertEqual(str(principal), principal.user.first_name + ' ' + principal.user.last_name)