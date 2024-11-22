# core/views.py
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Post
from django.views.generic import TemplateView

class FeedView(TemplateView):
    template_name = 'core/feed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            communities = self.request.user.communities_joined.all()
            posts = Post.objects.filter(community__in=communities).order_by('-created_at')
            context['posts'] = posts
        else:
            context['posts'] = None
        return context

class HomeView(TemplateView):
    template_name = 'core/home.html'