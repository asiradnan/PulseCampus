from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch
from django.core import signing

class UserSignalsTestCase(TestCase):
    @patch('users.signals.send_confirmation_email.delay')
    def test_user_created_signal(self, mock_send_confirmation_email_from_signals):
        user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com') 
        token = signing.dumps(user.email)
        mock_send_confirmation_email_from_signals.assert_called_once_with(user.email, token)