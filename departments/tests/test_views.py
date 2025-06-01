from django.test import TestCase
from django.contrib.auth.models import User
from departments.models import Department
from users.models import Principal
from django.urls import  reverse

class DepartmentViewTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.principal_user = User.objects.create_user(username='testuser', password='testpassword')
        self.principal = Principal.objects.create(user=self.principal_user, designation='Principal',joining_date='2023-01-01', address='123 Main St', room_number='101', building_number='202')
        self.other_user = User.objects.create_user(username='otheruser', password='testpassword')
        self.department = Department.objects.create(department_name='Computer Science', room_number='101', building_number='202')

    def test_principal_can_create_department(self):
        self.client.force_login(self.principal_user)
        response = self.client.post(reverse('departments:department_create'), {'department_name': 'Data Science', 'room_number': '101', 'building_number': '202'})
        self.assertEqual(response.status_code, 302)

    def test_other_than_principal_cannot_create_department(self):
        self.client.force_login(self.other_user)
        response = self.client.post(reverse('departments:department_create'), {'department_name': 'Science', 'room_number': '101', 'building_number': '202'})
        self.assertEqual(response.status_code, 403)

    def test_everyone_can_view_departments(self):
        response = self.client.get('/departments/')
        self.assertEqual(response.status_code, 200)

    def test_principal_can_update_department(self):
        self.client.force_login(self.principal_user)
        department = Department.objects.create(department_name='Test department_name', room_number='101', building_number='202')
        response = self.client.post(reverse('departments:department_update', args=[str(department.pk)]),
                                    {'department_name': 'Test department_name Updated', 'room_number': '101', 'building_number': '202'})
        self.assertEqual(response.status_code, 302)
        department.refresh_from_db()
        self.assertEqual(department.department_name, 'Test department_name Updated')
        
    def test_other_than_principal_cannot_update_department(self):
        self.client.force_login(self.other_user)
        department = Department.objects.create(department_name='Test department_name', room_number='101', building_number='202')
        self.client.post(reverse('departments:department_update', args=[str(department.pk)]),
                                    {'department_name': 'Test department_name Updated', 'room_number': '101', 'building_number': '202'})    
        department.refresh_from_db()
        self.assertNotEqual(department.department_name,"Team department_name Updated")   

    def test_department_delete(self):
        self.client.force_login(self.principal_user)
        department = Department.objects.create(department_name='Test department_name', room_number='101', building_number='202')
        response = self.client.post(reverse('departments:department_delete', args=[str(department.pk)]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Department.objects.filter(pk=department.pk).exists())

    def test_other_than_principal_cannot_delete_department(self):
        self.client.force_login(self.other_user)
        department = Department.objects.create(department_name='Test department_name', room_number='101', building_number='202')
        response = self.client.post(reverse('departments:department_delete', args=[str(department.pk)]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Department.objects.filter(pk=department.pk).exists())

    def test_department_detail_view(self):
        response = self.client.get(reverse('departments:department_detail', args=[str(self.department.pk)]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.department.department_name)
        self.assertContains(response, self.department.room_number)
        self.assertContains(response, self.department.building_number)
        self.assertIn('teachers', response.context)
