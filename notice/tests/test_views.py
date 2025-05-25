from django.test import TestCase, override_settings
from django.urls import reverse
from notice.models import Notice, User
from departments.models import Department
from users.models import Teacher
import os
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

class NoticeViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):  
        cls.department = Department.objects.create(department_name="Computer Science", room_number="101", building_number="1")
        cls.user = User.objects.create_user(username="testuser", password="kothinektapass", first_name="Test", last_name="User")  # Store user reference
        cls.teacher = Teacher.objects.create(
            user=cls.user, 
            department=cls.department,
            designation="Professor",
            address="123 Main St",
            joining_date="2022-01-01",
        )
    
    def test_teacher_can_create_notice(self):
        loggedin = self.client.login(username="testuser", password="kothinektapass")
        self.assertTrue(loggedin)
        response = self.client.post(reverse("notice:notice_create"), {"title": "New Notice", "content": "New Content"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Notice.objects.count(), 1)  

    def test_teacher_can_delete_notice(self):
        loggedin = self.client.login(username="testuser", password="kothinektapass")
        self.assertTrue(loggedin)
        notice = Notice.objects.create(title="Test Notice", content="Test Content", posted_by=self.teacher.user)
        response = self.client.post(reverse("notice:notice_delete", kwargs={"pk": notice.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Notice.objects.count(), 0)
    
    @override_settings(
        DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage',
        MEDIA_ROOT=os.path.join(settings.BASE_DIR, 'test_media')
    )
    def test_notice_with_static_pdf(self):
        test_pdf_path = os.path.join(settings.BASE_DIR, 'notice', 'tests', 'test_files', 'sample.pdf')
        
        with open(test_pdf_path, 'rb') as pdf_file:
            uploaded_file = SimpleUploadedFile(
                "sample.pdf",
                pdf_file.read(),
                content_type='application/pdf'
            )
            notice = Notice.objects.create(
                title = "Notice with Static PDF", 
                content = "Content with real PDF",
                pdf_file = uploaded_file,
                posted_by = self.teacher.user,
            )
            self.assertEqual(Notice.objects.count(), 1)
            with self.assertRaises(ValidationError):
                notice.full_clean()

        test_pdf_path2 = os.path.join(settings.BASE_DIR, 'notice', 'tests', 'test_files', 'small.pdf')
        with open(test_pdf_path2, 'rb') as pdf_file:
            uploaded_file = SimpleUploadedFile(
                "small.pdf",
                pdf_file.read(),
                content_type='application/pdf'
            )
            notice2 = Notice.objects.create (
                title = "Notice with Static PDF", 
                content = "Content with real PDF",
                pdf_file = uploaded_file,
                posted_by = self.teacher.user
            )
            self.assertEqual(Notice.objects.count(), 2)
            notice2.full_clean()


    
