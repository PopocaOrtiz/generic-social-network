import uuid

from django.db import models

from users.models import get_user_model, UserType


User = get_user_model()


class Post(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    author: UserType = models.ForeignKey(User, on_delete=models.CASCADE)  # type: ignore
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.first_name}: {self.content[:100]}"