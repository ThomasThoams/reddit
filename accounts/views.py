# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, View
from django.contrib.auth import login, logout
from .forms import SignUpForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

class DeleteAccountView(LoginRequiredMixin, View):
    template_name = 'accounts/delete_account.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Votre compte a été supprimé avec succès.')
        return redirect('home')

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)