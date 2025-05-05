from django.urls import path
from . import views 

app_name = 'clubs'  

urlpatterns = [
    path('create/',views.ClubCreateView.as_view(),name='club_create'),
    path('club_list/',views.ClubListView.as_view(),name='club_list'),
    path('<str:pk>/',views.ClubDetailView.as_view(),name='club_detail'),
    path('<str:pk>/update/',views.ClubUpdateView.as_view(),name='club_update'),
]