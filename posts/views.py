# posts/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm
from .models import Post, Vote
from django.views import View
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create_post.html'
    success_url = reverse_lazy('feed')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Passer l'utilisateur au formulaire
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

class VoteView(LoginRequiredMixin, View):
    def post(self, request, post_id, vote_type):
        post = get_object_or_404(Post, id=post_id)
        if vote_type in [1, -1]:
            Vote.objects.update_or_create(
                user=request.user,
                post=post,
                defaults={'vote_type': vote_type}
            )
        return redirect('post_detail', pk=post_id)