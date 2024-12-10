from django.db import models
from django.contrib.auth.models import User

class Repository(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    repo_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Repositório de {self.user.username} - {self.repo_url}'
    
