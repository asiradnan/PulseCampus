from django.db import models
from PulseCampus import validators

class Department(models.Model):
    name=models.CharField(max_length=100,primary_key=True)
    room_number=models.CharField(max_length=4,validators=[validators.all_digits])
    building_number=models.CharField(max_length=4,validators=[validators.all_digits])

    def __str__(self):
        return self.name
    def save(self, force_insert=False, force_update=False):
        self.name = self.name.title()
        super(Department, self).save(force_insert, force_update)
