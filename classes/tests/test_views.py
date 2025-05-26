from django.test import TestCase    
from django.urls import reverse
from classes.models import Class
from users.models import Principal, User, Teacher, Student

class ClassViewTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
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
        self.default_class = Class.objects.create(
            class_code='1',
            building_number='2',
            room_number='3'
        )
        self.student = Student.objects.create(
            user=User.objects.create_user(
                username='student',
                password='password',
                first_name = 'Jane',
                last_name = 'Doe'
            ),
            student_id='1234567890',
            address='123 Main St',
            student_class=self.default_class
        )
    
    def test_principal_can_create_class(self):
        self.client.login(username='principal', password='password')
        form_data  = {
            'class_code' : '2',
            'building_number' : '2',
            'room_number' : '3'
        }
        response = self.client.post(reverse('classes:class_create'),data=form_data)
        self.assertEqual(response.status_code,302)
        self.assertEqual(Class.objects.count(),2)
        self.assertTrue(Class.objects.filter(class_code='2').exists())

    def test_student_cannot_create_class(self):
        self.client.login(username='student', password='password')
        form_data  = {
            'class_code' : '1',
            'building_number' : '2',
            'room_number' : '3'
        }
        response = self.client.post(reverse('classes:class_create'),data=form_data)
        self.assertEqual(response.status_code,403)
        self.assertEqual(Class.objects.count(),1)

    def test_class_code_is_unique(self):
        self.client.login(username='principal', password='password')
        form_data  = {
            'class_code' : '1',
            'building_number' : '2',
            'room_number' : '3'
        }
        response = self.client.post(reverse('classes:class_create'),data=form_data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(Class.objects.count(),1)

    def test_class_list_view(self):
        response = self.client.get(reverse('classes:class_list'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'classes/class_list.html')
        self.assertContains(response,self.default_class.class_code)

    def test_class_detail_view(self):
        response = self.client.get(reverse('classes:class_detail',args=[self.default_class.pk]))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'classes/class_detail.html')
        self.assertContains(response,self.default_class.class_code)

    def test_class_update_view(self):
        self.client.login(username='principal', password='password')
        form_data  = {
            'class_code' : '1',
            'building_number' : '2',
            'room_number' : '4'
        }
        response = self.client.post(reverse('classes:class_update',args=[self.default_class.pk]),data=form_data)
        self.assertEqual(response.status_code,302)
        self.assertEqual(Class.objects.count(),1)
        self.assertEqual(Class.objects.get(pk=self.default_class.pk).class_code,'1')
        form_data  = {
            'class_code' : '2',
            'building_number' : '2',
            'room_number' : '4'
        }
        response = self.client.post(reverse('classes:class_update',args=[self.default_class.pk]),data=form_data)
        self.assertEqual(response.status_code,302)
        self.assertEqual(Class.objects.count(),1)
        self.assertEqual(Class.objects.get(pk=self.default_class.pk).class_code,'2')

    def test_class_delete_view(self):
        self.client.login(username='principal', password='password')
        response = self.client.post(reverse('classes:class_delete',args=[self.default_class.pk]))
        self.assertEqual(response.status_code,302)
        self.assertEqual(Class.objects.count(),0)

    def test_class_delete_otherthan_principal(self):
        self.client.login(username='student', password='password')
        response = self.client.post(reverse('classes:class_delete',args=[self.default_class.pk]))
        self.assertEqual(response.status_code,302)
        self.assertEqual(Class.objects.count(),1)

    def test_toggle_captain(self):
        self.client.login(username='principal', password='password')
        response = self.client.post(reverse('classes:toggle_captain',args=[self.default_class.pk]),data={'student_id':self.student.student_id})
        self.assertEqual(response.status_code,302)
        self.assertEqual(Student.objects.get(pk=self.student.pk).is_captain,True)
        response = self.client.post(reverse('classes:toggle_captain',args=[self.default_class.pk]),data={'student_id':self.student.student_id})
        self.assertEqual(response.status_code,302)
        self.assertEqual(Student.objects.get(pk=self.student.pk).is_captain,False)
