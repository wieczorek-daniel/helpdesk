from django.db import models
from django.contrib.auth.models import User

class Issue(models.Model):
    reporter = models.ForeignKey(User, related_name='reporter', on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name='assignee', on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    is_in_progress = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title