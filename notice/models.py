from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import FileExtensionValidator

class Notice(models.Model):
    posted_by=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    content=models.TextField(max_length=10000)
    pdf_file = models.FileField(upload_to='notices/', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])])
    date=models.DateField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('notice:notice_detail', kwargs={'pk': self.pk})
