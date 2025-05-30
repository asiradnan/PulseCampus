from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from . import forms
from django.db import transaction
from django.core import signing 
from .tasks import send_reset_email
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        is_active = True
        username_or_email = request.POST.get('username or email')
        password = request.POST.get('password')
        if '@' in username_or_email:
            try:
                email = username_or_email.lower().strip()
                user = User.objects.get(email=email)
                if user:
                    is_active = user.is_active
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                user = None
        else:
            user = User.objects.get(username=username_or_email)
            if user:
                is_active = user.is_active
            user = authenticate(request, username=username_or_email, password=password)
        if not is_active:
            messages.error(request, 'Your account is not active. Please confirm your email.')   
            return redirect('users:login')
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
    return _role_based_signup(request, forms.PrincipalForm)   

def verify_email(request, token):
    try:
        email = signing.loads(token, max_age=60*60*24)
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        messages.success(request, "Email verified successfully!")
    except signing.BadSignature:
        messages.error(request, "Invalid token.")
    return redirect('users:login')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = signing.dumps(email)
            send_reset_email.delay(email, token)
            messages.success(request, "Password reset email sent successfully!")
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
    return render(request, 'users/forgot_password.html')

def reset_password(request, token):
    try:
        email = signing.loads(token, max_age=60*60)
        user = User.objects.get(email=email)
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            try:
                validate_password(password)
            except ValidationError as e:
                messages.error(request, e.messages[0])
                return render(request, 'users/reset_password.html')
        
            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return render(request, 'users/reset_password.html')
            
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfully!")
            return redirect('users:login')
        else: 
            return render(request, 'users/reset_password.html')
        
    except signing.SignatureExpired:
        messages.error(request, "Token has expired.")
        return redirect('users:forgot_password')
    except signing.BadSignature:
        messages.error(request, "Invalid token.")
        return redirect('users:forgot_password')

@login_required 
def profile(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    if hasattr(request.user, 'student'):
        form_class = forms.StudentForm
        profile = request.user.student
    elif hasattr(request.user, 'teacher'):
        form_class = forms.TeacherForm
        profile = request.user.teacher
    elif hasattr(request.user, 'principal'):
        form_class = forms.PrincipalForm
        profile = request.user.principal
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile)
        form.fields.pop('password')
        form.fields.pop('confirm_password') 
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user = request.user
            try:
                with transaction.atomic():
                    user.first_name = first_name
                    user.last_name = last_name
                    user.username = username
                    user.email = email
                    user.save()
                    form.save()
                    messages.success(request, "Profile updated successfully!")
                    return redirect('users:profile')
            except Exception as e:
                messages.error(request, "An error occurred while updating the profile.")
                print(e)
                return render(request, 'users/profile.html', {'form': form})
    else:
        user_data = {
            'username':request.user.username,
            'email' : request.user.email,
            'first_name' : request.user.first_name,
            'last_name' : request.user.last_name
        }
        
        form = form_class(instance=profile, initial=user_data)
        form.fields.pop('password')
        form.fields.pop('confirm_password') 
        # print(form)
        # print(form_class)
    return render(request, 'users/profile.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user = request.user
        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect('users:profile')
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('users:profile')
        try:
            validate_password(new_password)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect('users:profile')
        user.set_password(new_password)
        user.save()
        messages.success(request, "Password changed successfully!")
        return redirect('users:profile')
    return redirect('users:profile')
    

def delete_account(request):
    user = request.user
    user.delete()
    messages.success(request, "Account deleted successfully!")
    return redirect('users:login')
