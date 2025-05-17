from django.test import TestCase
from ..models import Class

class ClassModelTestCase(TestCase):
    def setUp(self):
        self.class_1 = Class.objects.create(1,45, 12)