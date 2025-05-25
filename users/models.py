from django.db import models
from django.contrib.auth.models import User
from PulseCampus import validators
from classes.models import Class
from departments.models import Department

class Student(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    student_id=models.CharField(max_length=10,validators=[validators.id_validate], unique=True)
    student_class=models.ForeignKey(Class,on_delete=models.SET_NULL,null=True)
    address=models.TextField(max_length=500)
    is_captain=models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    def make_captain(self):
        self.is_captain = True
        self.save()
    def remove_captain(self):
        self.is_captain = False
        self.save()

class Teacher(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    # POSITION_CHOICES=[('Chairman','Chairman'),('Vice Chairman','Vice Chairman'),('Member','Member')]
    # dept_designation=models.CharField(max_length=100, choices=POSITION_CHOICES)
    joining_date=models.DateField(validators=[validators.no_future_date])
    address=models.TextField(max_length=500)
    designation=models.CharField(max_length=100,validators=[validators.no_digit])

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name



class Principal(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    POSITION_CHOICES=[('Principal','Principal'),('Vice Principal','Vice Principal')]
    designation=models.CharField(max_length=100, choices=POSITION_CHOICES)
    joining_date=models.DateField(validators=[validators.no_future_date])
    address=models.TextField(max_length=500)
    room_number=models.CharField(max_length=4,validators=[validators.all_digits])
    building_number=models.CharField(max_length=4,validators=[validators.all_digits])

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

