from django.db import models
from django.contrib.auth.models import User

class Issue(models.Model):
    reporter = models.ForeignKey(User, related_name='reporter', on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name='assignee', on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()
    solution = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS = (
        ('to_do', ('Nierozpoczęte')),
        ('in_progress', ('W realizacji')),
        ('testing', ('Testowanie')),
        ('done', ('Ukończone')),
    )

    status = models.CharField(max_length=32, choices=STATUS, default='to_do')
    
    def __str__(self):
        return self.title