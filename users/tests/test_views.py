from django.test import TestCase, override_settings
from django.urls import reverse
from users.models import User, Student 
from classes.models import Class
from unittest.mock import patch
from django.core import mail

@override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        CELERY_TASK_ALWAYS_EAGER=True  
    )
class UsersViewTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
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
        self.assertEqual(len(mail.outbox), 1)   
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Welcome to PulseCampus')
        token = email.body.split('verify_email/')[1].split(' Note that')[0].strip()
        self.assertFalse(User.objects.get(email='student@test.com').is_active)
        response = self.client.get(reverse('users:verify_email', args=[token+'bad_token']))
        self.assertFalse(User.objects.get(email='student@test.com').is_active)
        response = self.client.get(reverse('users:verify_email', args=[token]))
        self.assertTrue(User.objects.get(email='student@test.com').is_active)


    def test_email_as_username(self):
        temp_class = Class.objects.create(class_code = '1A', building_number = '1', room_number = '1')
        self.assertEqual(Class.objects.count(),1)
        form_data = {
            'first_name' : 'test',
            'last_name' : 'user',
            'username' : 'student@test.com',
            'email' : 'student@test.com',
            'password': 'p1q2w3e4r',
            'confirm_password': 'p1q2w3e4r',
            'student_class' : temp_class.pk,
            'student_id':'123456',
            'address':  'test address'
        }
        count = User.objects.count()
        response = self.client.post(reverse('users:student_signup'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/role_based_signup.html')
        self.assertEqual(User.objects.count(),count)

    def test_invalid_passwrd_confirmation(self):
        temp_class = Class.objects.create(class_code = '1A', building_number = '1', room_number = '1')
        self.assertEqual(Class.objects.count(),1)
        form_data = {
            'first_name' : 'test',
            'last_name' : 'user',
            'username' : 'student',
            'email' : 'student@test.com',
            'password': '1234',
            'confirm_password': '1234',
            'student_class' : temp_class.pk,
            'student_id':'123456',
            'address':  'test address'
        }
        count = User.objects.count()
        response = self.client.post(reverse('users:student_signup'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/role_based_signup.html')
        self.assertEqual(User.objects.count(),count)

    def test_unmatched_passwords(self):
        temp_class = Class.objects.create(class_code = '1A', building_number = '1', room_number = '1')
        self.assertEqual(Class.objects.count(),1)
        form_data = {
            'first_name' : 'test',
            'last_name' : 'user',
            'username' : 'student',
            'email' : 'student@test.com',
            'password': 'p1q2w3e4r',
            'confirm_password': 'p1q2w3e4rrrrrrrrr',
            'student_class' : temp_class.pk,
            'student_id':'123456',
            'address':  'test address'
        }
        count = User.objects.count()
        response = self.client.post(reverse('users:student_signup'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/role_based_signup.html')
        self.assertEqual(User.objects.count(),count)

    def test_taken_username(self):
        temp_class = Class.objects.create(class_code = '1A', building_number = '1', room_number = '1')
        self.assertEqual(Class.objects.count(),1)
        form_data = {
            'first_name' : 'test',
            'last_name' : 'user',
            'username' : 'testuser',
            'email' : 'student@test.com',
            'password': 'p1q2w3e4r',
            'confirm_password': 'p1q2w3e4r',
            'student_class' : temp_class.pk,
            'student_id':'123456',
            'address':  'test address'
        }
        count = User.objects.count()
        response = self.client.post(reverse('users:student_signup'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/role_based_signup.html')
        self.assertEqual(User.objects.count(),count)

    def test_taken_email(self):
        temp_class = Class.objects.create(class_code = '1A', building_number = '1', room_number = '1')
        self.assertEqual(Class.objects.count(),1)
        form_data = {
            'first_name' : 'test',
            'last_name' : 'user',
            'username' : 'student',
            'email' : 'test@test.com',
            'password': 'p1q2w3e4r',
            'confirm_password': 'p1q2w3e4r',
            'student_class' : temp_class.pk,
            'student_id':'123456',
            'address':  'test address'
        }
        count = User.objects.count()
        response = self.client.post(reverse('users:student_signup'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/role_based_signup.html')
        self.assertEqual(User.objects.count(),count)

    def test_profile(self):
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
            'student_id':'123457',
            'address':  'test address'
        }
        response = self.client.post(reverse('users:student_signup'), data=form_data)
        user = User.objects.get(username='student')
        user.is_active = True
        user.save()
        logged_in = self.client.login(username='student', password='p1q2w3e4r')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

        form_data['last_name'] = 'updated'
        response = self.client.post(reverse('users:profile'), data=form_data)
        self.assertRedirects(response, reverse('users:profile'))
        self.assertEqual(User.objects.get(username='student').last_name, 'updated')

    def test_forgot_password(self):
        form_data = {
            'email' : 'test@test.com'
        }
        response = self.client.post(reverse('users:forgot_password'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/forgot_password.html')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Password Reset')
        token = mail.outbox[0].body.split('reset_password/')[1].strip()
        response = self.client.get(reverse('users:reset_password', args=[token]))
        self.assertTemplateUsed(response, 'users/reset_password.html')
        form_data = {
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }
        response = self.client.post(reverse('users:reset_password', args=[token]), data=form_data)
        self.assertTemplateUsed(response, 'users/reset_password.html')
        form_data = {
            'password': 'p11q2w3e4r',
            'confirm_password': 'p11q2w3e4rrrrr'
        }
        response = self.client.post(reverse('users:reset_password', args=[token]), data=form_data)
        self.assertTemplateUsed(response, 'users/reset_password.html')
        form_data = {
            'password': 'p11q2w3e4r',
            'confirm_password': 'p11q2w3e4r'
        }
        response = self.client.post(reverse('users:reset_password', args=[token]), data=form_data)
        self.assertRedirects(response, reverse('users:login'))

    def test_nonexistent_email_forgot_password(self):
        form_data = {
            'email' : 'nonexistent@test.com'
        }
        response = self.client.post(reverse('users:forgot_password'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/forgot_password.html')

    def test_password_change_view(self):
        form_data = {
            'old_password': 'pass1234',
            'new_password': 'p1q2w3e4r',
            'confirm_password': 'p1q2w3e4r'
        }
        loggedin = self.client.login(username='testuser', password='pass1234')
        self.assertTrue(loggedin)
        response = self.client.post(reverse('users:change_password'), data=form_data)
        self.assertEqual(User.objects.get(username='testuser').check_password('p1q2w3e4r'), True)

    def test_delete_account(self):
        loggedin = self.client.login(username='testuser', password='pass1234')
        self.assertTrue(loggedin)
        response = self.client.get(reverse('users:delete_account'))
        self.assertEqual(User.objects.count(), 0)



