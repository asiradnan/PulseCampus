from django.test import TestCase
from departments.models import Department
from django.core.exceptions import ValidationError

class DepartmentModelTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.department=Department.objects.create(department_name="Computer Science",room_number="101",building_number="1")

    def test_stringify(self):
        self.assertEqual(str(self.department),self.department.department_name)

    def test_room_number_cannot_be_empty(self):
        deparment = Department(department_name="Computer Science",room_number="",building_number="1")
        with self.assertRaises(ValidationError):
            deparment.full_clean()
