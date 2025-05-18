from django.test import TestCase
from django.urls import reverse
from users.models import User, Student 
from classes.models import Class

class UsersViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password = 'pass1234')
        self.user.email="test@test.com"
        self.user.save()

    def test_logged_in_user_login_view(self):
        self.assertEqual(User.objects.count(),1)
        loggedin = self.client.login(username=self.user.username, password = 'pass1234')
        
        response = self.client.get(reverse('users:login'))
        self.assertTrue(loggedin)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, expected_url=reverse('homepage'), status_code=302, target_status_code=200)

    def test_get_login_view(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_post_login_view_with_username(self):
        form_data = {
            'username or email' : 'testuser',
            'password' : 'pass1234'
        }
        response = self.client.post(reverse('users:login'),data=form_data)
        self.assertRedirects(response, expected_url=reverse('homepage'), status_code=302, target_status_code=200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_with_wrong_password(self):
        form_data = {
            'username or email' : 'testuser',
            'password' : 'pass12345'
        }
        response = self.client.post(reverse('users:login'),data=form_data)
        self.assertRedirects(response, expected_url=reverse('users:login'), status_code=302, target_status_code=200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_view_with_email(self):
        form_data = {
            'username or email' : 'test@test.com',
            'password' : 'pass1234'
        }
        response = self.client.post(reverse('users:login'), data=form_data)
        self.assertRedirects(response, expected_url=reverse('homepage'), status_code=302, target_status_code=200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_with_nonexistent_email(self):
        form_data = {
            'username or email' : 'test1@test.com',
            'password' : 'pass1234'
        }
        response = self.client.post(reverse('users:login'), data=form_data)
        self.assertRedirects(response, expected_url=reverse('users:login'), status_code=302, target_status_code=200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_view(self):
        loggedin = self.client.login(username = self.user.username, password = 'pass1234')
        self.assertTrue(loggedin)
        response = self.client.get(reverse('users:logout'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_signup_view(self):
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')

    def test_student_signup_view(self):
        response = self.client.get(reverse('users:student_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/role_based_signup.html')

    def test_teacher_signup_view(self):
        response = self.client.get(reverse('users:teacher_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/role_based_signup.html')

    def test_principal_signup_view(self):
        response = self.client.get(reverse('users:principal_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/role_based_signup.html')

    def test_student_signup(self):
        temp_class = Class.objects.create(class_code = '1A', building_number = '1', room_number = '1')
        self.assertEqual(Class.objects.count(),1)
        form_data = {
            'first_name' : 'test',
            'last_name' : 'user',
            'username' : 'student',
            'email' : 'student@test.com',
            'password': 'p1q2w3e4r',
            'confirm_password': 'p1q2w3e4r',
            'student_class' : temp_class.pk,
            'student_id':'123456',
            'address':  'test address'
        }
        response = self.client.post(reverse('users:student_signup'), data=form_data)
        self.assertRedirects(response, expected_url=reverse('users:login'), status_code=302, target_status_code=200)
        self.assertEqual(User.objects.count(),2)
        self.assertEqual(Student.objects.count(),1)
