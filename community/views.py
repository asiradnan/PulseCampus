from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView
from .models import Post, Comment, Vote
from .forms import PostForm 
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required   
from django.db.models import Count, Case, When, IntegerField
from django.contrib.messages.views import SuccessMessageMixin   

@method_decorator(ratelimit(key='ip', rate='30/d', method=['POST']), name='post')
class PostCreateView(SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    success_message = "Post created successfully."

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        print(form.instance)
        return super().form_valid(form)

@method_decorator(ratelimit(key='ip', rate='30/d', method=['POST']), name='post')
class PostUpdateView(SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_message = "Post updated successfully."

class PostDetailView(DetailView):
    model = Post

    def get_queryset(self):
        return Post.objects.select_related('posted_by').prefetch_related(
            'comments__commented_by',
            'vote_set'
        )
    
class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.annotate(
            upvote_count=Count(
                Case(When(vote__upvote=True, then=1), output_field=IntegerField())
            ),
            downvote_count=Count(
                Case(When(vote__downvote=True, then=1), output_field=IntegerField())
            ),
            vote_score=Count(
                Case(When(vote__upvote=True, then=1), output_field=IntegerField())
            ) - Count(
                Case(When(vote__downvote=True, then=1), output_field=IntegerField())
            ),
            comment_count=Count('comments', distinct=True)
        ).select_related(
            'posted_by',
            'posted_by__student',
            'posted_by__teacher', 
            'posted_by__principal'
        ).order_by('-time')

def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    messages.success(request, 'Post deleted successfully.')
    return redirect('community:post_list')

def add_comment(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(post=post, commented_by=request.user, content=content)
    messages.success(request, 'Comment added successfully.')
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

@login_required
def upvote(request, pk):
    post = Post.objects.get(pk=pk)
    vote, flag = Vote.objects.get_or_create(post=post, user=request.user)
    vote.upvote = True
    vote.downvote = False
    vote.save()
    messages.success(request, 'Upvoted successfully.')
    return redirect('community:post_detail', pk=pk)

@login_required
def downvote(request, pk):
    post = Post.objects.get(pk=pk)
    vote, flag = Vote.objects.get_or_create(post=post, user=request.user)
    vote.upvote = False
    vote.downvote = True
    vote.save()
    messages.success(request, 'Downvoted successfully.')
    return redirect('community:post_detail', pk=pk)