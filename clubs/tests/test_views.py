from django.test import TestCase
from django.urls import reverse
from users.models import Principal, User, Teacher, Student
from clubs.models import Club
from departments.models import Department

class ClubViewTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.teacher = Teacher.objects.create(
            user=User.objects.create_user(
                username='teacher',
                password='password',
                first_name = 'John',
                last_name = 'Doe'
            ),
            department = Department.objects.create(
                department_name = 'Computer Science',
                building_number = '1',
                room_number = '1'
            ),
            address='123 Main St',
            joining_date = '2025-02-03',
            designation = 'Teacher'
        )
        

    def test_teacher_can_create_club(self):
        self.client.login(username='teacher', password='password')
        form_data  = {
            'club_name' : 'Club A',
            'established' : '2023-01-01',
            'description' : 'This is a test club'
        }
        response = self.client.post(reverse('clubs:club_create'),data=form_data)
        self.assertTrue(Club.objects.filter(club_name='Club A').exists())
        self.assertEqual(Club.objects.count(),1)
        self.assertEqual(Club.objects.first().supervisor, self.teacher)
        self.assertEqual(str(Club.objects.first()), 'Club A')