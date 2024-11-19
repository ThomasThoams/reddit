# social/views.py
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm, PostForm, CommunityForm
from .models import User, Community, Post, Vote

def home(request):
    if request.user.is_authenticated:
        return redirect('feed')
    return render(request, 'social/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = SignUpForm()
    return render(request, 'social/signup.html', {'form': form})

class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'social/login.html'

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Votre compte a été supprimé avec succès.')
        return redirect('home')
    return render(request, 'social/delete_account.html')

@login_required
def profile(request):
    user = request.user
    num_comments = user.comments.count()
    num_posts = user.posts.count()
    num_upvoted_posts = user.votes.filter(vote_type=1).count()

    context = {
        'user': user,
        'num_comments': num_comments,
        'num_posts': num_posts,
        'num_upvoted_posts': num_upvoted_posts,
    }
    return render(request, 'social/profile.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm(request.user)
    return render(request, 'social/create_post.html', {'form': form})

@login_required
def create_community(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.creator = request.user
            community.save()
            community.members.add(request.user)  # Le créateur rejoint automatiquement
            return redirect('community_detail', pk=community.pk)
    else:
        form = CommunityForm()
    return render(request, 'social/create_community.html', {'form': form})

@login_required
def community_list(request):
    communities = Community.objects.all()
    return render(request, 'social/community_list.html', {'communities': communities})

@login_required
def community_detail(request, pk):
    community = get_object_or_404(Community, pk=pk)
    posts = community.posts.all().order_by('-created_at')
    is_member = community in request.user.communities_joined.all()
    return render(request, 'social/community_detail.html', {
        'community': community,
        'posts': posts,
        'is_member': is_member
    })

@login_required
def join_community(request, pk):
    community = get_object_or_404(Community, pk=pk)
    community.members.add(request.user)
    return redirect('community_detail', pk=pk)

@login_required
def leave_community(request, pk):
    community = get_object_or_404(Community, pk=pk)
    community.members.remove(request.user)
    return redirect('community_list')

@login_required
def feed(request):
    communities = request.user.communities_joined.all()
    posts = Post.objects.filter(community__in=communities).order_by('-created_at')
    return render(request, 'social/feed.html', {'posts': posts})

@login_required
def vote(request, post_id, vote_type):
    post = get_object_or_404(Post, id=post_id)
    if vote_type in [1, -1]:
        Vote.objects.update_or_create(
            user=request.user,
            post=post,
            defaults={'vote_type': vote_type}
        )
    return redirect('feed')

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user_vote = post.votes.filter(user=request.user).first()
    return render(request, 'social/post_detail.html', {'post': post, 'user_vote': user_vote})
