import uuid

from django.db import models
from django.core.exceptions import ValidationError

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

    image = models.URLField(null=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.first_name}: {self.content[:100]}"


class Comment(Base):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, related_name='comments')

    def save(self, *args, **kwargs):

        if self.post is None and self.comment is None:
            raise ValidationError('comment must be assigned to another comment or a post')

        super().save(*args, **kwargs)

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
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.type} {self.post.content[:20]}"
    

class Report(models.Model):

    TYPES = (
        ('SPAM', 'spam'),
        ('INAPPROPRIATE', 'inappropriate'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=TYPES)
    user: UserType = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # type: ignore
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='reports')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if self.post and self.post.author is self.user:
            raise ValidationError('user cant report own post')

        super().save(*args, **kwargs)

    def __str__(self):
        if self.post:
            return f"post {self.post.id} was reported for {self.type}"
        if self.comment:
            return f"comment {self.comment.id} was reported for {self.type}"
        
        raise ValidationError('report must be assigned to a post or a comment')
    

class SavedPost(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user: UserType = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # type: ignore
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"post {self.post.id} was saved"