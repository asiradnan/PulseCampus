from django.test import TestCase
from django.contrib.auth.models import User
from .models import Principal, Teacher
from django.utils import timezone
from departments.models import Department

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
        principal.full_clean() 
        self.assertEqual(principal.user, user)
        self.assertEqual(principal.designation, 'Principal')
        self.assertEqual(principal.joining_date, timezone.now().date())
        self.assertEqual(principal.address, '123 Main St')
        self.assertEqual(principal.room_number, '1010')
        self.assertEqual(principal.building_number, '2020')
        self.assertEqual(principal.user.username, 'testuser')
        self.assertEqual(str(principal), principal.user.first_name + ' ' + principal.user.last_name)

class TeacherFlowTest(TestCase):
    def setup(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.department = Department.objects.create(name='Computer Science', room_number='101', building_number='202')
        self.teacher = Teacher.objects.create(
            user=self.user,
            designation='Teacher',
            joining_date=timezone.now().date(),
            address='123 Main St',
            department='Computer Science'
        )
    def test_teacher_creation(self):
        self.assertEqual(self.teacher.user, self.user)
        self.assertEqual(self.teacher.designation, 'Teacher')
        self.assertEqual(self.teacher.joining_date, timezone.now().date())
        self.assertEqual(self.teacher.address, '123 Main St')
        self.assertEqual(self.teacher.department, 'Computer Science')
        self.assertEqual(str(self.teacher), self.teacher.user.first_name + ' ' + self.teacher.user.last_name)