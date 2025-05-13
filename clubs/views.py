from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from .models import Club, Membership
from .forms import ClubForm
from PulseCampus.mixins import TeacherOrPrincipalRequiredMixin

class ClubCreateView(TeacherOrPrincipalRequiredMixin, CreateView):
    model = Club
    form_class = ClubForm

    def form_valid(self, form):
        form.instance.supervisor = self.request.user.teacher
        return super().form_valid(form)

class ClubListView(ListView):
    model = Club

class ClubDetailView(DetailView):
    model = Club

class ClubUpdateView(TeacherOrPrincipalRequiredMixin, UpdateView):
    model = Club
    form_class = ClubForm