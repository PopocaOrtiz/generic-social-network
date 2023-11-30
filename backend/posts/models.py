import uuid

from django.db import models

from users.models import get_user_model, UserType


User = get_user_model()


class Base(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author: UserType = models.ForeignKey(User, on_delete=models.CASCADE)  # type: ignore
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Post(Base):
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.first_name}: {self.content[:100]}"


class Comment(Base):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"{self.author.first_name} {self.content}"
    

class Reaction(models.Model):

    TYPES = (
        ('LIKE', 'like'),
        ('DISLIKE', 'dislike'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=TYPES)
    user: UserType = models.ForeignKey(User, on_delete=models.CASCADE)  # type: ignore
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.type} {self.post.content[:20]}"