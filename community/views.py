from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DeleteView, DetailView, ListView
from .models import Post, Comment
from .forms import PostForm 

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm

class PostDetailView(DetailView):
    model = Post

class PostListView(ListView):
    model = Post

class PostDeleteView(DeleteView):
    model = Post