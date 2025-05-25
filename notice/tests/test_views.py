from django.test import TestCase
from django.urls import reverse
from notice.models import Notice, User
from departments.models import Department
from users.models import Teacher

class NoticeListViewTestCase(TestCase):
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
