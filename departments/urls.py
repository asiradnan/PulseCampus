from django.urls import path
from . import views

app_name = "departments"

urlpatterns = [
   path("create/", views.DepartmentCreateView.as_view(),name="department_create"),
   path("<str:pk>/", views.DepartmentDetailView.as_view(),name="department_detail"),
   path("", views.DepartmentListView.as_view(),name="department_list"),
   path("<str:pk>/update/", views.DepartmentUpdateView.as_view(),name="department_update"),
   
]