from django.test import TestCase
from django.contrib.auth.models import User
from .models import Principal, Teacher
from django.utils import timezone
from departments.models import Department
from django.db.utils import IntegrityError
from django.urls import reverse

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
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.department = Department.objects.create(department_name='Computer Science', room_number='101', building_number='202')
        self.teacher = Teacher.objects.create(
            user=self.user,
            designation='Teacher',
            joining_date=timezone.now().date(),
            address='123 Main St',
            department=self.department
        )
        self.user3 = User.objects.create_user(username='testuser3', password='testpassword')
    def test_teacher_creation(self):
        self.assertEqual(self.teacher.user, self.user)
        self.assertEqual(self.teacher.designation, 'Teacher')
        self.assertEqual(self.teacher.joining_date, timezone.now().date())
        self.assertEqual(self.teacher.address, '123 Main St')
        self.assertEqual(self.teacher.department.department_name, 'Computer Science')
        self.assertEqual(str(self.teacher), self.teacher.user.first_name + ' ' + self.teacher.user.last_name)
        self.assertEqual(self.teacher.user.username, 'testuser')

    def test_teacher_department_cannot_be_null(self):
        with self.assertRaises(IntegrityError):
            Teacher.objects.create(
                user=self.user3,
                designation='Teacher',
                joining_date=timezone.now().date(),
                address='123 Main St',
                department=None
            )

    def test_teacher_department_cannot_be_invalid(self):
        with self.assertRaises(Department.DoesNotExist):
            Teacher.objects.create(
                user=self.user3,
                designation='Teacher',
                joining_date=timezone.now().date(),
                address='123 Main St',
                department=Department.objects.get(pk = 10)
            )

    # def test_teacher_update_view(self):        
    #     self.client.force_login(self.user)
    #     response = self.client.post(reverse('teacher_update', args=[self.teacher.pk]),{
    #         'designation': 'Teacher',
    #         'joining_date': timezone.now().date(),
    #         'address': '456 Main St',
    #         'department': self.department,
    #     })
    #     self.assertEqual(response.status_code, 302)
        
    # def test_other_teacher_cannot_update_teacher_account(self):
    #     self.client.force_login(self.user3)
    #     response = self.client.post(reverse('teacher_update', args=[self.teacher.pk]),{
    #         'designation': 'Teacher',
    #         'joining_date': timezone.now().date(),
    #         'address': '456 Main St',
    #         'department': self.department,
    #     })
    #     self.assertEqual(response.status_code, 403)
    
    # def test_teacher_delete_account(self):
    #     self.client.force_login(self.user)
    #     response = self.client.post(reverse('teacher_delete', args=[self.teacher.pk]))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(Teacher.objects.count(), 1)
    #     self.assertEqual(Department.objects.count(), 1)
    #     self.assertEqual(User.objects.count(), 1)
    #     self.assertEqual(User.objects.get(username='testuser').is_active, False)

    




