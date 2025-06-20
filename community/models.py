from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PulseCampus.validators import file_less_than_2mb
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

class Post(models.Model):
    posted_by=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=300, validators=[MinLengthValidator(1)])
    content=models.TextField(max_length=10000)
    image = models.ImageField(upload_to='images/',null=True,blank=True, validators=[file_less_than_2mb])
    time = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('community:post_detail', args=[str(self.pk)])   
    
    def get_vote_count(self):
        return self.vote_set.filter(upvote=True).count() - self.vote_set.filter(downvote=True).count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.content

class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upvote = models.BooleanField(default=False)
    downvote = models.BooleanField(default=False)

    def clean(self):
        if self.upvote and self.downvote:
            raise ValidationError("Upvote and downvote cannot be true simultaneously.")