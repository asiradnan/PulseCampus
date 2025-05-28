from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .models import Department
from PulseCampus.mixins import PrincipalRequiredMixin


class DepartmentListView(ListView):
    model = Department

class DepartmentCreateView(PrincipalRequiredMixin, CreateView):
    model = Department
    fields = "__all__"
    def test_func(self):
        return hasattr(self.request.user, 'principal')

class DepartmentDetailView(DetailView):
    model = Department

class DepartmentUpdateView(UpdateView):
    model = Department
    fields = "__all__"
