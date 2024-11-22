# posts/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostForm
from .models import Post, Vote
from django.views import View
from django.shortcuts import get_object_or_404, redirect

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
    def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = self.object
                comment.author = request.user
                parent_id = request.POST.get('parent_id')
                if parent_id:
                    comment.parent = Comment.objects.get(id=parent_id)
                comment.save()
                return redirect('post_detail', pk=self.object.pk)
            return self.get(request, *args, **kwargs)

class VoteView(LoginRequiredMixin, View):
    def post(self, request, post_id, vote_type):
        post = get_object_or_404(Post, id=post_id)
        vote_type = int(vote_type)
        # Vérifier que vote_type est bien 1 ou -1
        if vote_type in [1, -1]:
            # Logique pour gérer les votes
            if vote_type == 1:
                post.upvotes.add(request.user)
                post.downvotes.remove(request.user)
            elif vote_type == -1:
                post.downvotes.add(request.user)
                post.upvotes.remove(request.user)
            post.score = post.upvotes.count() - post.downvotes.count()
            post.save()
        next_url = request.POST.get('next', 'home')
        return redirect(next_url)
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('feed')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class SearchResultsView(ListView):
    model = Post
    template_name = 'posts/search_results.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('query')
        return Post.objects.filter(title__icontains=query)