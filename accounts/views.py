# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from .forms import SignUpForm
from .models import User

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
