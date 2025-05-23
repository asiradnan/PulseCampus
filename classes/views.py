from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from . import models
from PulseCampus.mixins import PrincipalRequiredMixin
from django.contrib.auth.decorators import login_required
from PulseCampus.mixins import is_principal
from django.contrib import messages

class CreateClassView(PrincipalRequiredMixin,CreateView):
    model = models.Class
    fields = "__all__"

class ClassListView(ListView):
    model = models.Class

class ClassDetailView(DetailView):
    model = models.Class    

class ClassUpdateView(PrincipalRequiredMixin, UpdateView):
    model = models.Class
    fields = "__all__"

@login_required
def class_delete(request, pk):
    if not is_principal(request.user):
        messages.error(request, 'You are not authorized to delete this class.')   
        return redirect('classes:class_detail', pk=pk)  
    if request.method == 'POST':
        class_obj = models.Class.objects.get(pk=pk)
        class_obj.delete()
        return redirect('classes:class_list')
