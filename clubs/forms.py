from django import forms
from .models import Club

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['club_name','established'] 

        widgets = {
            'established': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_club_name(self):
        club_name = self.cleaned_data.get('club_name')
        if Club.objects.filter(club_name=club_name).exists():
            raise forms.ValidationError('A club with this name already exists.')
        return club_name