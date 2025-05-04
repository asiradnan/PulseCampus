from django.shortcuts import render, redirect
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

def class_delete(request, pk):
    if request.method == 'POST':
        class_obj = models.Class.objects.get(pk=pk)
        class_obj.delete()
        return redirect('classes:class_list')
