from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    posted_by=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField(max_length=10000)
    image = models.ImageField(upload_to='images/',null=True,blank=True)
    time = models.DateTimeField(auto_now_add=True, editable=False)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True, editable=False)
