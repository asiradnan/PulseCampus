from django.test import TestCase
from django.contrib.auth.models import User
from .models import Department
from users.models import Principal
from django.urls import  reverse

class DepartmentTest(TestCase):
    def setUp(self):
        self.principal_user = User.objects.create_user(username='testuser', password='testpassword')
        self.principal = Principal.objects.create(user=self.principal_user, designation='Principal',joining_date='2023-01-01', address='123 Main St', room_number='101', building_number='202')
        self.other_user = User.objects.create_user(username='otheruser', password='testpassword')
        self.department = Department.objects.create(name='Computer Science', room_number='101', building_number='202')

    def test_principal_can_create_department(self):
        self.client.force_login(self.principal_user)
        response = self.client.post(reverse('departments:department_create'), {'name': 'Data Science', 'room_number': '101', 'building_number': '202'})
        self.assertEqual(response.status_code, 302)

    def test_other_than_principal_cannot_create_department(self):
        self.client.force_login(self.other_user)
        response = self.client.post(reverse('departments:department_create'), {'name': 'Science', 'room_number': '101', 'building_number': '202'})
        self.assertEqual(response.status_code, 403)

    def test_everyone_can_view_departments(self):
        response = self.client.get('/departments/')
        self.assertEqual(response.status_code, 200)

    def test_principal_can_update_department(self):
        self.client.force_login(self.principal_user)
        department = Department.objects.create(name='Test Name', room_number='101', building_number='202')
        response = self.client.post(reverse('departments:department_update', args=[str(department.pk)]),
                                    {'name': 'Test Name Updated', 'room_number': '101', 'building_number': '202'})
        self.assertEqual(response.status_code, 302)
        department.refresh_from_db()
        self.assertEqual(department.name, 'Test Name Updated')
        
    def test_other_than_principal_cannot_update_department(self):
        self.client.force_login(self.other_user)
        department = Department.objects.create(name='Test Name', room_number='101', building_number='202')
        self.client.post(reverse('departments:department_update', args=[str(department.pk)]),
                                    {'name': 'Test Name Updated', 'room_number': '101', 'building_number': '202'})    
        department.refresh_from_db()
        self.assertNotEqual(department.name,"Team Name Updated")                              
