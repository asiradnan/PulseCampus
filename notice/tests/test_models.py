from django.test import TestCase    
from notice.models import Notice, User
from django.core.exceptions import ValidationError

class NoticeModelTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user=User.objects.create(username="testuser", password="testpassword")

    def test_only_teacher_or_principal_can_post_notice(self):
        notice = Notice(posted_by=self.user, title="Test Notice", content="Test Content")
        with self.assertRaises(ValidationError):
            notice.clean()
