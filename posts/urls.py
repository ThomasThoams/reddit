# posts/urls.py
from django.urls import path, register_converter
from .views import PostCreateView, PostDetailView, VoteView

class IntConverter:
    regex = '-?\d+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)

register_converter(IntConverter, 'negint')

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/vote/<negint:vote_type>/', VoteView.as_view(), name='vote'),
    # ... autres URL patterns
]
