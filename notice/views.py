from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import DetailView, DeleteView 
from .models import Notice
from .forms import NoticeForm
from PulseCampus.mixins import TeacherOrPrincipalRequiredMixin
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

class NoticeListView(ListView):
    model = Notice

@method_decorator(ratelimit(key='ip', rate='30/d', block=True), name='post') 
class NoticeCreateView(TeacherOrPrincipalRequiredMixin, CreateView):
    model = Notice
    form_class = NoticeForm

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)
    
class NoticeDetailView(DetailView):
    model = Notice

@method_decorator(ratelimit(key='ip', rate='30/d', block=True), name='post') 
class NoticeUpdateView(TeacherOrPrincipalRequiredMixin, UpdateView):
    model = Notice
    form_class = NoticeForm

def delete_notice(request, pk):
    notice = Notice.objects.get(pk=pk)
    notice.delete()
    return redirect('notice:notice_list')

