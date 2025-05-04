from django import forms
from . import models

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(min_length=1, max_length=250)
    last_name = forms.CharField(min_length=1, max_length=250)
    username = forms.CharField(min_length=1, max_length=250)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = models.Student
        fields = ['student_id', 'student_class', 'address']
    field_order = ['first_name','last_name', 'username', 'email', 'password', 'confirm_password', 'student_id', 'student_class', 'address']

class TeacherForm(forms.ModelForm):
    first_name = forms.CharField(min_length=1, max_length=250)
    last_name = forms.CharField(min_length=1, max_length=250)
    username = forms.CharField(min_length=1, max_length=250)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = models.Teacher
        fields = ['department', 'joining_date', 'address', 'designation']
        widgets = {
            'joining_date': forms.widgets.DateInput(attrs={'type': 'date'})
        }
    field_order = ['first_name','last_name', 'username', 'email', 'password', 'confirm_password', 'department', 'joining_date', 'address', 'designation']
        
class PrincipalForm(forms.ModelForm):
    first_name = forms.CharField(min_length=1, max_length=250)
    last_name = forms.CharField(min_length=1, max_length=250)
    username = forms.CharField(min_length=1, max_length=250)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = models.Principal
        fields = ['designation', 'joining_date', 'address', 'room_number', 'building_number']
        widgets = {
            'joining_date': forms.widgets.DateInput(attrs={'type': 'date'})
        }
    field_order = ['first_name','last_name', 'username', 'email','password', 'confirm_password', 'name', 'designation', 'joining_date', 'address', 'room_number', 'building_number']  