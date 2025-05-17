from django.db import models
from PulseCampus import validators
from django.urls import reverse
from django.core.validators import MinLengthValidator

class Class(models.Model):
    class_code=models.CharField(max_length=2,unique=True, validators=[MinLengthValidator(1)] )
    room_number=models.CharField(max_length=3,validators=[validators.all_digits])
    building_number=models.CharField(max_length=2,validators=[validators.all_digits])

    class Meta:
        constraints = [
            models.CheckConstraint(condition = ~models.Q(class_code=''), name='class code can not be empty'),
        ]


    def __str__(self):
        return self.class_code
    
    def get_absolute_url(self):
        return reverse('classes:class_detail', args=[str(self.pk)])
