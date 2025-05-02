from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Department

class DepartmentListView(ListView):
    model = Department