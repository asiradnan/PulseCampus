from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from . import models
from PulseCampus.mixins import PrincipalRequiredMixin
from django.contrib.auth.decorators import login_required
from PulseCampus.mixins import is_principal
from django.contrib import messages
from users.models import Student
from django.contrib.messages.views import SuccessMessageMixin

class CreateClassView(PrincipalRequiredMixin,SuccessMessageMixin, CreateView):
    model = models.Class
    fields = "__all__"
    success_message = "Class created successfully"

class ClassListView(ListView):
    model = models.Class

class ClassDetailView(DetailView):
    model = models.Class    

class ClassUpdateView(PrincipalRequiredMixin, SuccessMessageMixin, UpdateView):
    model = models.Class
    fields = "__all__"
    success_message = "Class updated successfully"

@login_required
def class_delete(request, pk):
    if not is_principal(request.user):
        messages.error(request, 'You are not authorized to delete this class.')   
        return redirect('classes:class_detail', pk=pk)  
    if request.method == 'POST':
        class_obj = models.Class.objects.get(pk=pk)
        class_obj.delete()
        messages.success(request, 'Class deleted successfully.')
        return redirect('classes:class_list')
    
def toggle_captain(request, pk):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        selected_student = Student.objects.get(student_id=student_id)
        make_captain = not selected_student.is_captain
        students_of_the_class = Student.objects.filter(student_class = selected_student.student_class)
        for student in students_of_the_class:
            if student == selected_student:
                student.is_captain = make_captain
            else:
                student.is_captain = not make_captain
            student.save()
    return redirect('classes:class_detail', pk=pk)
