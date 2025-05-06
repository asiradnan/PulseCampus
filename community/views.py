from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DeleteView, DetailView, ListView
from .models import Post, Comment

class PostCreateView(CreateView):
    model = Post
    fields = '__all__'

class PostUpdateView(UpdateView):
    model = Post
    fields = '__all__'

class PostDetailView(DetailView):
    model = Post

class PostListView(ListView):
    model = Post

class PostDeleteView(DeleteView):
    model = Post