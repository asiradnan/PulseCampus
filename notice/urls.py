from django.urls import path
from . import views

app_name = 'notice'

urlpatterns = [
    path('', views.NoticeListView.as_view(), name='notice_list'),
    path('create/', views.NoticeCreateView.as_view(), name='notice_create'),
    path('<str:pk>/', views.NoticeDetailView.as_view(), name='notice_detail'),
    path('<str:pk>/update/', views.NoticeUpdateView.as_view(), name='notice_update'),
    path('<str:pk>/delete/', views.delete_notice, name='notice_delete'),
]