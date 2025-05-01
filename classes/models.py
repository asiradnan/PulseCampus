from django.db import models
from PulseCampus import validators

class Class(models.Model):
    class_code=models.CharField(max_length=4,primary_key=True)
    room_number=models.CharField(max_length=4,validators=[validators.all_digits])
    building_number=models.CharField(max_length=4,validators=[validators.all_digits])

    def __str__(self):
        return self.class_code
