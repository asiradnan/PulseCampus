from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DeleteView, DetailView, ListView
from .models import Post, Comment
from .forms import PostForm 
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required   

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

def add_comment(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(post=post, commented_by=request.user, content=content)
    return redirect('community:post_detail', pk=pk)

@login_required
def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    if comment.commented_by == request.user:
        comment.delete()
    else:
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect('community:post_detail', pk=comment.post.pk)
    messages.success(request, 'Comment deleted successfully.')
    return redirect('community:post_detail', pk=comment.post.pk)