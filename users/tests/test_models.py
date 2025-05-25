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
    @classmethod
    def setUpTestData(cls):
        cls.class_eleven = Class.objects.create(
            class_code = '11',
            building_number = '1',
            room_number = '2'
        )
        cls.student = Student.objects.create(
            user=User.objects.create_user(
                username='student',
                password='password',
                first_name = 'Jane',
                last_name = 'Doe'
            ),
            address='456 Oak St',
            student_id='123456',
            student_class = cls.class_eleven
        )

    def test_student_creation(self):
        self.assertEqual(Student.objects.count(), 1)
        self.student.student_id = '1234567890'
        with self.assertRaises(ValidationError):
            self.student.full_clean()
    
    def test_student_make_captain(self):
        self.assertFalse(self.student.is_captain)
        self.student.make_captain()
        self.assertTrue(self.student.is_captain)

    def test_student_remove_captain(self):
        self.student.make_captain()
        self.assertTrue(self.student.is_captain)
        self.student.remove_captain()
        self.assertFalse(self.student.is_captain)


class TeacherModelTestCase(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            department_name = 'Computer Science',
            room_number = '1',
            building_number = '2'
        )
        self.assertEqual(Department.objects.count(), 1)
        self.teacher = Teacher.objects.create(
            user=User.objects.create_user(
                username='teacher',
                password='password',
                first_name = 'John',
                last_name = 'Doe'
            ),
            address='789 Maple St',
            department = self.department,
            joining_date = '2025-02-03',
            designation = 'Professor'
        )


    def test_teacher_creation(self):
        self.teacher.full_clean()
        self.teacher.designation = '12'
        with self.assertRaises(ValidationError):
            self.teacher.full_clean()
        self.teacher.designation = 'Professor'
        self.teacher.full_clean()
        self.teacher.joining_date = '3025-02-04'
        with self.assertRaises(ValidationError):
            self.teacher.full_clean()
        self.assertEqual(Teacher.objects.count(), 1)

    def test_teacher_stringify(self):
        self.assertEqual(str(self.teacher), 'John Doe')


