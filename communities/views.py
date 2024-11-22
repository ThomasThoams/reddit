# communities/views.py
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Community
from .forms import CommunityForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect

class CommunityListView(LoginRequiredMixin, ListView):
    model = Community
    template_name = 'communities/community_list.html'
    context_object_name = 'communities'

class CommunityCreateView(LoginRequiredMixin, CreateView):
    model = Community
    form_class = CommunityForm
    template_name = 'communities/create_community.html'
    success_url = reverse_lazy('community_list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)
        form.instance.members.add(self.request.user)
        return response

class CommunityDetailView(LoginRequiredMixin, DetailView):
    model = Community
    template_name = 'communities/community_detail.html'
    context_object_name = 'community'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        community = self.get_object()
        context['posts'] = community.posts.all().order_by('-created_at')
        context['is_member'] = self.request.user in community.members.all()
        return context

class JoinCommunityView(LoginRequiredMixin, View):
    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        community.members.add(request.user)
        return redirect('community_detail', pk=pk)

class LeaveCommunityView(LoginRequiredMixin, View):
    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        community.members.remove(request.user)
        return redirect('community_list')
