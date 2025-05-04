from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView, DeleteView
from . import models

class CreateClassView(CreateView):
    model = models.Class
    fields = "__all__"

class ClassListView(ListView):
    model = models.Class

class ClassDetailView(DetailView):
    model = models.Class    

class ClassUpdateView(UpdateView):
    model = models.Class
    fields = "__all__"

class ClassDeleteView(DeleteView):
    model = models.Class
