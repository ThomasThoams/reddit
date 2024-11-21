# communities/models.py
from django.db import models
from django.conf import settings

class Community(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='communities_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name