from django.test import TestCase
from .models import Class

class TestClassModel(TestCase):
    def setUp(self):
        self.test_class = Class(class_code="CS101")
        
    def test_str_representation(self):
        self.assertEqual(str(self.test_class), "CS101")
        
    def test_str_representation_empty(self):
        empty_class = Class(class_code="")
        self.assertEqual(str(empty_class), "")
        
    def test_str_representation_special_chars(self):
        special_class = Class(class_code="CS-101#")
        self.assertEqual(str(special_class), "CS-101#")
        
    def test_str_representation_numbers(self):
        number_class = Class(class_code="12345")
        self.assertEqual(str(number_class), "12345")