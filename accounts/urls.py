# accounts/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import SignUpView
from .forms import LoginForm
from . import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(authentication_form=LoginForm, template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
