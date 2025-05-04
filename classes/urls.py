from django.urls import path
from . import views

app_name = 'classes'    

urlpatterns = [
    path('create/',views.CreateClassView.as_view(),name='class_create'),
    path('class_list/',views.ClassListView.as_view(),name='class_list'),
    path('<str:pk>/',views.ClassDetailView.as_view(),name='class_detail'),
    path('<str:pk>/update/',views.ClassUpdateView.as_view(),name='class_update'),
    path('<str:pk>/delete/',views.class_delete,name='class_delete'),
]