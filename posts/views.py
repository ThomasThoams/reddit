# posts/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostForm, CommentForm  
from .models import Post, Vote, Comment
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render, redirect

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create_post.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Passer l'utilisateur au formulaire
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

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
        else:
            context = self.get_context_data()
            context['comment_form'] = form
            return self.render_to_response(context)

class VoteView(LoginRequiredMixin, View):
    def post(self, request, post_id, vote_type):
        post = get_object_or_404(Post, id=post_id)
        vote_type = int(vote_type)
        if vote_type in [1, -1]:
            # Retirer l'utilisateur des votes existants
            post.upvotes.remove(request.user)
            post.downvotes.remove(request.user)
            if vote_type == 1:
                post.upvotes.add(request.user)
            elif vote_type == -1:
                post.downvotes.add(request.user)
            # Plus besoin de mettre à jour le champ 'score'
        next_url = request.POST.get('next', 'home')
        return redirect(next_url)
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('home')

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