from django.db import models
from PulseCampus import validators
from django.urls import reverse
from django.core.exceptions import ValidationError


class Department(models.Model):
    department_name=models.CharField(max_length=100,unique=True)
    room_number=models.CharField(max_length=4,validators=[validators.all_digits])
    building_number=models.CharField(max_length=4,validators=[validators.all_digits])

    def clean(self):
        if self.room_number == "" or self.building_number == "":
            raise ValidationError("Room number and building number cannot be empty")
    
    def __str__(self):
        return self.department_name
    
    def get_absolute_url(self):
        return reverse("departments:department_detail", kwargs={"pk": self.pk})
