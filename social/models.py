# social/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    communities_joined = models.ManyToManyField('Community', related_name='members')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Community(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name='communities_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')
    community = models.ForeignKey('Community', on_delete=models.CASCADE, related_name='posts')

    def score(self):
        return self.votes.aggregate(total=Sum('vote_type'))['total'] or 0

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'Commentaire de {self.author.email} sur {self.post.title}'

class Vote(models.Model):
    VOTE_TYPES = (
        (1, 'Upvote'),
        (-1, 'Downvote'),
    )
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='votes')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='votes')
    vote_type = models.IntegerField(choices=VOTE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.get_vote_type_display()} par {self.user.email} sur {self.post.title}'
