from django.db import models
from django.contrib.auth.models import User
from PulseCampus import validators
from classes.models import Class

class Student(models.Model):
    user=models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=255,validators=[validators.name_validator])
    student_id=models.CharField(max_length=10,validators=[validators.id_validate])
    student_class=models.ForeignKey(Class,on_delete=models.SET_NULL,null=True)
    address=models.TextField(max_length=500)
    is_captain=models.BooleanField(default=False)

    def __str__(self):
        return self.name
    def make_captain(self):
        self.is_captain = True
        self.save()
    def save(self,*args, **kwargs):
        self.name = self.name.title()
        super().save(*args, **kwargs)
