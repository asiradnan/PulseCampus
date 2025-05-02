from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from . import forms

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user  = authenticate(request, username = username, password = password)
        if not user:
            messages.add_message(request, messages.ERROR, 'Invalid username or password')
            return redirect('login')
        login(request, user)
        return redirect('home')

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
                messages.add_message(request, messages.ERROR, "Passwords do not match!")
                return render(request,'role_based_signup.html',{'form':form})
            try:
                validate_password(password)
            except ValidationError as e:
                messages.error(request, e.messages[0])
                return render(request,'role_based_signup.html',{'form':form})
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
            profile.user = user
            profile.save()
            return redirect('login')
        else:
            messages.add_message(request, messages.ERROR, "Form is not valid!")
    else:
        form = form_class()
    return render(request,'role_based_signup.html',{'form':form})   

def student_signup(request):
    return _role_based_signup(request, forms.StudentForm)    
    
def teacher_signup(request):
    return _role_based_signup(request, forms.TeacherForm)   
    
def principal_signup(request):
    return _role_based_signup(request, forms.PrincipalForm)     