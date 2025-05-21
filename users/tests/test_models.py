from django.test import TestCase
from users.models import User, Principal, Student, Teacher
from classes.models import Class
from departments.models import Department
from django.core.exceptions import ValidationError

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

    


class StudentModelTestCase(TestCase):
    def setUp(self):
        pass

    def test_student_creation(self):
        class_eleven = Class.objects.create(
            class_code = '11',
            building_number = '1',
            room_number = '2'
        )
        self.assertEqual(Class.objects.count(), 1)  
        student = Student.objects.create(
            user=User.objects.create_user(
                username='student',
                password='password',
                first_name = 'Jane',
                last_name = 'Doe'
            ),
            address='456 Oak St',
            student_id='1234567890',
            student_class = class_eleven
        )
        with self.assertRaises(ValidationError):
            student.full_clean()
        self.assertEqual(Student.objects.count(), 1)


class TeacherModelTestCase(TestCase):
    def setUp(self):
        pass

    def test_teacher_creation(self):
        department = Department.objects.create(
            department_name = 'Computer Science',
            room_number = '1',
            building_number = '2'
        )
        self.assertEqual(Department.objects.count(), 1)
        teacher = Teacher.objects.create(
            user=User.objects.create_user(
                username='teacher',
                password='password',
                first_name = 'John',
                last_name = 'Doe'
            ),
            address='789 Maple St',
            department = department,
            joining_date = '2025-02-03',
            designation = 'Professor'
        )
        teacher.full_clean()
        teacher.designation = '12'
        with self.assertRaises(ValidationError):
            teacher.full_clean()
        teacher.designation = 'Professor'
        teacher.full_clean()
        teacher.joining_date = '3025-02-04'
        with self.assertRaises(ValidationError):
            teacher.full_clean()
        self.assertEqual(Teacher.objects.count(), 1)


