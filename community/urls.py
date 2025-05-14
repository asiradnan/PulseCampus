from django.urls import path
from . import views

app_name = 'community'  

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<str:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<str:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('<str:pk>/delete/', views.delete_post, name='post_delete'),
    path('<str:pk>/comment/', views.add_comment, name='add_comment'),   
]