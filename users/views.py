from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from . import forms

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user  = authenticate(request, username = username, password = password)
        if not user:
            messages.error(request, 'Invalid username or password')
            return redirect('/users/login/')
        login(request, user)
        return redirect('home')
    return render(request, 'login.html')

def signup(request):
    return render(request,'signup.html')

def _role_based_signup(request, form_class):
    if request.method == 'POST':
        form =  form_class(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return render(request,'role_based_signup.html',{'form':form})
            if User.objects.filter(username = username).exists():
                messages.error(request, "Username already exists!")
                return render(request,'role_based_signup.html',{'form':form})
            if User.objects.filter(email = email).exists():
                messages.error(request, "Email already exists!")
                return render(request,'role_based_signup.html',{'form':form})
            try:
                validate_password(password)
            except ValidationError as e:
                messages.error(request, e.messages[0])
                return render(request,'role_based_signup.html',{'form':form})
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
            profile.user = user
            profile.save()
            messages.success(request, "Account created successfully!")
            return redirect('/users/login/')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = form_class()
    return render(request,'role_based_signup.html',{'form':form})   

def student_signup(request):
    return _role_based_signup(request, forms.StudentForm)    
    
def teacher_signup(request):
    return _role_based_signup(request, forms.TeacherForm)   
    
def principal_signup(request):
    return _role_based_signup(request, forms.PrincipalForm)     