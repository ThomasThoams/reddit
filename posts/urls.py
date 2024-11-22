# posts/urls.py
from django.urls import path
from .views import PostCreateView, PostDetailView, VoteView

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/vote/<int:vote_type>/', VoteView.as_view(), name='vote'),
]
