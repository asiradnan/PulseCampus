from django.test import TestCase
from django.urls import reverse
from users.models import User

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

    def test_login_view_with_email(self):
        form_data = {
            'username or email' : 'test@test.com',
            'password' : 'pass1234'
        }
        response = self.client.post(reverse('users:login'), data=form_data)
        self.assertRedirects(response, expected_url=reverse('homepage'), status_code=302, target_status_code=200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
