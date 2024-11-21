# core/views.py
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Post
from django.views.generic import TemplateView

class FeedView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'core/feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        communities = self.request.user.communities_joined.all()
        return Post.objects.filter(community__in=communities).order_by('-created_at')

class HomeView(TemplateView):
    template_name = 'core/home.html'