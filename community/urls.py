from django.urls import path
from . import views

app_name = 'community'  

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<str:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<str:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('<str:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]