from django import forms
from .models import Club

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['club_name','established'] 

        widgets = {
            'established': forms.DateInput(attrs={'type': 'date'}),
        }