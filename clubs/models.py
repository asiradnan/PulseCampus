from django.db import models
from PulseCampus import validators  
from django.urls import reverse

class Club(models.Model):
    club_name = models.CharField(max_length=100, unique=True)
    established=models.DateField(validators=[validators.no_future_date])
    supervisor = models.ForeignKey('users.Teacher', on_delete=models.CASCADE)

    def __str__(self):
        return self.club_name
    
    def save(self,*args,**kwargs):
        self.club_name=self.club_name.title()
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('clubs:club_detail', args=[str(self.pk)])

class Membership(models.Model):
    POSITION_CHOICES = [
        ('Member', 'Member'),
        ('President', 'President'),
        ('Vice President', 'Vice President'),
        ('Secretary', 'Secretary'),
        ('Treasurer', 'Treasurer'),
    ]

    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)