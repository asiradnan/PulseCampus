from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('signup/',views.signup,name='signup'),
    path('signup/student/',views.student_signup,name='student_signup'),
    path('signup/teacher/',views.teacher_signup,name='teacher_signup'),
    path('signup/principal/',views.principal_signup,name='principal_signup'),
    path('verify_email/<str:token>/',views.verify_email,name='verify_email'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('reset_password/<str:token>/',views.reset_password,name='reset_password'),
    path('profile/',views.profile,name='profile'),
    path('change_password/',views.change_password,name='change_password'),
    path('delete_account/',views.delete_account,name='delete_account'),
    
]