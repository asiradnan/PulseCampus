from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DeleteView, DetailView, ListView
from .models import Post, Comment
from .forms import PostForm 
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

@method_decorator(ratelimit(key='ip', rate='30/d', method=['POST']), name='post')
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        print(form.instance)
        return super().form_valid(form)

@method_decorator(ratelimit(key='ip', rate='30/d', method=['POST']), name='post')
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