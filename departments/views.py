from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from .models import Department
from PulseCampus.mixins import PrincipalRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages 
from django.contrib.messages.views import SuccessMessageMixin

class DepartmentListView(ListView):
    model = Department

class DepartmentCreateView(SuccessMessageMixin, PrincipalRequiredMixin, CreateView):
    model = Department
    fields = "__all__"
    success_message = "Department created successfully"
    def test_func(self):
        return hasattr(self.request.user, 'principal')

class DepartmentDetailView(DetailView):
    model = Department
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers'] = self.object.teacher_set.all()
        return context

class DepartmentUpdateView(SuccessMessageMixin, UpdateView):
    model = Department
    fields = "__all__"
    success_message = "Department updated successfully"

def department_delete(request, pk):
    if not hasattr(request.user, 'principal'):
        return redirect("home")
    department = Department.objects.get(pk=pk)
    department.delete()
    messages.success(request, "Department deleted successfully")
    return redirect("departments:department_list")
