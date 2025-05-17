from django.test import TestCase
from ..models import Class
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class ClassModelTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.class_1 = Class.objects.create(class_code = '1', building_number = '2', room_number = '3')
    
    def test_stringify(self):
        self.assertEqual(str(self.class_1),'1')

    def test_class_code_can_not_be_empty(self):
        class_with_empty_class_code = Class(class_code = '',building_number = '2', room_number = '3')
        with self.assertRaises(IntegrityError): 
            class_with_empty_class_code.save()
    
    def test_class_code_can_not_be_null(self):
        class_with_empty_class_code = Class(building_number = '2', room_number = '3')
        with self.assertRaises(IntegrityError): 
            class_with_empty_class_code.save()

    def test_class_code_length_is_inclusively_between_one_and_two(self):
        class_with_long_class_code = Class(class_code = '123', building_number = '1', room_number = '3')
        with self.assertRaises(ValidationError): 
            class_with_long_class_code.full_clean()
        class_with_valid_class_code = Class(class_code = '12', building_number = '1', room_number = '3')    
        class_with_valid_class_code.full_clean()

    def test_building_number_length_is_inclusively_between_one_and_two(self):
        class_with_empty_building_number = Class(class_code = '12', building_number = '', room_number = '3')
        with self.assertRaises(ValidationError):
            class_with_empty_building_number.full_clean()
        class_without_building_number = Class(class_code = '12', room_number = '3') 
        with self.assertRaises(ValidationError):
            class_without_building_number.full_clean()
        class_with_long_building_number = Class(class_code = '12', building_number = '123', room_number = '3')
        with self.assertRaises(ValidationError):
            class_with_long_building_number.full_clean()
        class_with_valid_building_number = Class(class_code = '12', building_number = '1', room_number = '3')
        class_with_valid_building_number.full_clean()

    def test_building_number_can_not_be_negative(self):
        class_with_negative_building_number = Class(class_code = '12', building_number = '-1', room_number = '3')
        with self.assertRaises(ValidationError):
            class_with_negative_building_number.full_clean()

    def test_room_number_length_is_inclusively_between_one_and_three(self):
        class_with_empty_room_number = Class(class_code = '12', building_number = '1', room_number = '')
        with self.assertRaises(ValidationError):
            class_with_empty_room_number.full_clean()
        class_without_room_number = Class(class_code = '12', building_number = '1')
        with self.assertRaises(ValidationError):
            class_without_room_number.full_clean()
        class_with_long_room_number = Class(class_code = '12', building_number = '1', room_number = '1234')
        with self.assertRaises(ValidationError):
            class_with_long_room_number.full_clean()
        class_with_valid_room_number = Class(class_code = '12', building_number = '1', room_number = '1')
        class_with_valid_room_number.full_clean()
        class_with_valid_room_number = Class(class_code = '12', building_number = '1', room_number = '12')
        class_with_valid_room_number.full_clean()
        class_with_valid_room_number = Class(class_code = '12', building_number = '1', room_number = '123')
        class_with_valid_room_number.full_clean()

    def test_room_number_can_not_be_negative(self):
        class_with_negative_room_number = Class(class_code = '12', building_number = '1', room_number = '-1')
        with self.assertRaises(ValidationError):
            class_with_negative_room_number.full_clean()