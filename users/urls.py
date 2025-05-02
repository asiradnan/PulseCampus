from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('signup/student/',views.student_signup,name='student_signup'),
    path('signup/teacher/',views.teacher_signup,name='teacher_signup'),
    path('signup/principal/',views.principal_signup,name='principal_signup'),
]