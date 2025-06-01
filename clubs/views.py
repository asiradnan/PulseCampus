from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from .models import Club, Membership
from .forms import ClubForm
from PulseCampus.mixins import TeacherOrPrincipalRequiredMixin
from users.models import Student    
from django.contrib import messages 
from django.db import IntegrityError

class ClubCreateView(TeacherOrPrincipalRequiredMixin, CreateView):
    model = Club
    form_class = ClubForm

    def form_valid(self, form):
        form.instance.supervisor = self.request.user.teacher
        try:
            response = super().form_valid(form)
            messages.success(self.request, "Club created successfully.")
            return response
        except IntegrityError:
            form.add_error('club_name', 'A club with this name already exists.')
            return self.form_invalid(form)


class ClubListView(ListView):
    model = Club

class ClubDetailView(DetailView):
    model = Club
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['positions'] = Membership.POSITION_CHOICES
        context['members'] = Membership.objects.filter(club=self.object)
        return context

class ClubUpdateView(TeacherOrPrincipalRequiredMixin, UpdateView):
    model = Club
    form_class = ClubForm

def club_membership(request, pk):
    club = Club.objects.get(pk=pk)
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        position = request.POST.get('position')
        student = Student.objects.get(student_id=student_id)
        Membership.objects.create(student=student, club=club, position=position)
    return redirect('clubs:club_detail', pk=pk)