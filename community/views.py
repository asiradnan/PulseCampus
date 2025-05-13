from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DeleteView, DetailView, ListView
from .models import Post, Comment
from .forms import PostForm 

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        print(form.instance)
        return super().form_valid(form)

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm

class PostDetailView(DetailView):
    model = Post

class PostListView(ListView):
    model = Post

def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('community:post_list')