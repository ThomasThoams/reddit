# communities/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CommunityListView.as_view(), name='community_list'),
    path('create/', views.CommunityCreateView.as_view(), name='create_community'),
    path('<int:pk>/', views.CommunityDetailView.as_view(), name='community_detail'),
    path('<int:pk>/join/', views.JoinCommunityView.as_view(), name='join_community'),
    path('<int:pk>/leave/', views.LeaveCommunityView.as_view(), name='leave_community'),
]
