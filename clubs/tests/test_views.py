from django.test import TestCase
from django.urls import reverse
from users.models import Principal, User, Teacher, Student
from clubs.models import Club, Membership
from departments.models import Department
from classes.models import Class

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

    def test_membership(self):
        self.client.login(username='teacher', password='password')
        club = Club.objects.create(club_name='Club B', established='2023-01-01', supervisor=self.teacher)
        student = Student.objects.create(
            user=User.objects.create_user(
                username='student',
                password='password',
                first_name = 'Jane',
                last_name = 'Doe'
            ),
            student_id='123456',
            address='123 Main St',
            student_class= Class.objects.create(
                class_code='1',
                building_number='2',
                room_number='3'
            )
        )
        self.assertEqual(Student.objects.count(), 1)
        print(student.user.first_name)  
        form_data = {
            'student_id': student.student_id,
            'position': 'President'
        }
        response = self.client.post(reverse('clubs:club_membership', args=[club.pk]), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Membership.objects.count(), 1)
        self.assertEqual(Membership.objects.first().student, student)
        print(str(Membership.objects.first()))
        self.assertEqual(str(Membership.objects.first()), f"{student.user.first_name} {student.user.last_name} - President - {club.club_name}")

    def test_club_detail(self):
        self.client.login(username='teacher', password='password')
        club = Club.objects.create(club_name='Club C', established='2023-01-01', supervisor=self.teacher)
        response = self.client.get(reverse('clubs:club_detail', args=[club.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, club.club_name)
        self.assertIn('positions', response.context)
        self.assertEqual(response.context['positions'], Membership.POSITION_CHOICES)
        self.assertIn('members', response.context)
        self.assertEqual(list(response.context['members']), list(Membership.objects.filter(club=club)))
        self.assertEqual(response.context['club'], club)
