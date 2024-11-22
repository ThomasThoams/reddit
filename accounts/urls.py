from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from .views import SignUpView, ProfileView, DeleteAccountView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=LoginForm,
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('delete_account/', DeleteAccountView.as_view(), name='delete_account'),
]
