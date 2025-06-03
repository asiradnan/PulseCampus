from django.views.generic.base import TemplateView
from departments.models import Department
from classes.models import Class
from users.models import Teacher, Student

class HomePageView(TemplateView):
    template_name = 'homepage.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers'] = Teacher.objects.count() 
        context['students'] = Student.objects.count()
        context['departments'] = Department.objects.count()