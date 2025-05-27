from django import forms
from . import models
from django.contrib.auth.models import User

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=1, 
        max_length=250,
        widget=forms.TextInput(attrs={
            'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
            'placeholder': 'Enter first name'
        })
    )
    last_name = forms.CharField(
        min_length=1, 
        max_length=250,
        widget=forms.TextInput(attrs={
            'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
            'placeholder': 'Enter last name'
        })
    )
    username = forms.CharField(
        min_length=1, 
        max_length=250,
        widget=forms.TextInput(attrs={
            'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
            'placeholder': 'Choose a username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
            'placeholder': 'Create a password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
            'placeholder': 'Re-enter your password'
        })
    )
    
    class Meta:
        model = models.Student
        fields = ['student_id', 'student_class', 'address']
        widgets = {
            'student_id': forms.TextInput(attrs={
                'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
                'placeholder': 'Enter student ID'
            }),
            'student_class': forms.Select(attrs={
                'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 bg-white text-base'
            }),
            'address': forms.Textarea(attrs={
                'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition resize-none',
                'rows': 3,
                'cols': 40,
                'placeholder': 'Type your address'
            })
        }
    
    field_order = ['first_name','last_name', 'username', 'email', 'password', 'confirm_password', 'student_id', 'student_class', 'address']

class TeacherForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=1, 
        max_length=250,
        widget=forms.TextInput(attrs={
            'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
            'placeholder': 'Enter first name'
        })
    )
    last_name = forms.CharField(
        min_length=1, 
        max_length=250,
        widget=forms.TextInput(attrs={
            'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
            'placeholder': 'Enter last name'
        })
    )
    username = forms.CharField(
        min_length=1, 
        max_length=250,
        widget=forms.TextInput(attrs={
            'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
            'placeholder': 'Choose a username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
            'placeholder': 'Create a password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
            'placeholder': 'Re-enter your password'
        })
    )
    
    class Meta:
        model = models.Teacher
        fields = ['department', 'joining_date', 'address', 'designation']
        widgets = {
            'department': forms.Select(attrs={
                'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 bg-white text-base'
            }),
            'joining_date': forms.widgets.DateInput(attrs={
                'type': 'date',
                'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition'
            }),
            'address': forms.Textarea(attrs={
                'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition resize-none',
                'rows': 3,
                'cols': 40,
                'placeholder': 'Type your address'
            }),
            'designation': forms.Select(attrs={
                'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 bg-white text-base'
            })
        }
    
    field_order = ['first_name','last_name', 'username', 'email', 'password', 'confirm_password', 'department', 'joining_date', 'address', 'designation']
        
class PrincipalForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=1, 
        max_length=250,
        widget=forms.TextInput(attrs={
            'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
            'placeholder': 'Enter first name'
        })
    )
    last_name = forms.CharField(
        min_length=1, 
        max_length=250,
        widget=forms.TextInput(attrs={
            'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
            'placeholder': 'Enter last name'
        })
    )
    username = forms.CharField(
        min_length=1, 
        max_length=250,
        widget=forms.TextInput(attrs={
            'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
            'placeholder': 'Choose a username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
            'placeholder': 'Create a password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
            'placeholder': 'Re-enter your password'
        })
    )
    
    class Meta:
        model = models.Principal
        fields = ['designation', 'joining_date', 'address', 'room_number', 'building_number']
        widgets = {
            'designation': forms.Select(attrs={
                'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 bg-white text-base'
            }),
            'joining_date': forms.widgets.DateInput(attrs={
                'type': 'date',
                'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition'
            }),
            'address': forms.Textarea(attrs={
                'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition resize-none',
                'rows': 3,
                'cols': 40,
                'placeholder': 'Type your address'
            }),
            'room_number': forms.TextInput(attrs={
                'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
                'placeholder': 'Eg: 120A'
            }),
            'building_number': forms.TextInput(attrs={
                'class': 'rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-400 focus:border-blue-500 px-4 py-2 text-base bg-white outline-none transition',
                'placeholder': 'Eg: B2'
            })
        }
    
    field_order = ['first_name','last_name', 'username', 'email','password', 'confirm_password', 'designation', 'joining_date', 'address', 'room_number', 'building_number']  

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name','username', 'email']
