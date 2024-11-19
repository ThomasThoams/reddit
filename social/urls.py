# social/urls.py
from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('profile/', views.profile, name='profile'),
    path('feed/', views.feed, name='feed'),
    path('create_post/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/vote/<int:vote_type>/', views.vote, name='vote'),
    path('communities/', views.community_list, name='community_list'),
    path('communities/create/', views.create_community, name='create_community'),
    path('communities/<int:pk>/', views.community_detail, name='community_detail'),
    path('communities/<int:pk>/join/', views.join_community, name='join_community'),
    path('communities/<int:pk>/leave/', views.leave_community, name='leave_community'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
