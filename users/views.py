from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from . import forms
from django.db import transaction

def login_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        username_or_email = request.POST.get('username or email')
        password = request.POST.get('password')
        if '@' in username_or_email:
            try:
                email = username_or_email.lower().strip()
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                user = None
        else:
            user = authenticate(request, username=username_or_email, password=password)
        if user is None:
            messages.error(request, 'Invalid credentials.')
            return redirect('users:login')
        messages.success(request, 'Logged in successfully!')   
        login(request, user)
        return redirect('homepage')
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect(request.GET.get('next', '/'))

def signup(request):
    return render(request,'users/signup.html')

def _role_based_signup(request, form_class):
    if request.method == 'POST':
        form =  form_class(request.POST)
        if form.is_valid():
            try:
                # Start a transaction
                with transaction.atomic():
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    username = form.cleaned_data['username']
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    confirm_password = form.cleaned_data['confirm_password']
                    
                    if '@' in username and '.' in username.split('@')[1]:
                        messages.error(request, "Your username appears to be an email address. Please use a simple username.")
                        return render(request,'users/role_based_signup.html',{'form':form})
                    
                    try:
                        validate_password(password)
                    except ValidationError as e:
                        messages.error(request, e.messages[0])
                        return render(request,'users/role_based_signup.html',{'form':form})
                    
                    if password != confirm_password:
                        messages.error(request, "Passwords do not match!")
                        return render(request,'users/role_based_signup.html',{'form':form})
                    
                    if User.objects.filter(username=username).exists():
                        messages.error(request, "Username already exists!")
                        return render(request,'users/role_based_signup.html',{'form':form})
                    
                    if User.objects.filter(email=email).exists():
                        messages.error(request, "Email already exists!")
                        return render(request,'users/role_based_signup.html',{'form':form})
                    
                    email = email.lower().strip()
                    user = User.objects.create_user(
                        username=username, 
                        password=password, 
                        first_name=first_name, 
                        last_name=last_name, 
                        email=email
                    )
                    
                    profile = form.save(commit=False)
                    profile.user = user
                    profile.save()  # This is where the role creation happens
                    
                    messages.success(request, "Account created successfully!")
                    return redirect('users:login')
                    
            except Exception as e:
                messages.error(request, f"An error occurred during registration.")
                print(e)
                return render(request,'users/role_based_signup.html',{'form':form})
    else:
        form = form_class()
    return render(request,'users/role_based_signup.html',{'form':form})   

def student_signup(request):
    return _role_based_signup(request, forms.StudentForm)    
    
def teacher_signup(request):
    return _role_based_signup(request, forms.TeacherForm)   
    
def principal_signup(request):
    from .tasks import test
    test.delay('Hello, Celery!')
    return _role_based_signup(request, forms.PrincipalForm)     