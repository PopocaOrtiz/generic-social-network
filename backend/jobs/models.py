from typing import Any

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class JobApplication(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')
    
    def save(self, *args, **kwargs) -> None:
        
        if self.user == self.job.user:
            raise ValidationError("You can't apply to your own job")
        
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user} applied to {self.job}"
    

class Job(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title