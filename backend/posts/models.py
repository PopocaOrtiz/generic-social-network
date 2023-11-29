from django.db import models

from users.models import get_user_model, UserType


User = get_user_model()


class Post(models.Model):

    author: UserType = models.ForeignKey(User, on_delete=models.CASCADE)  # type: ignore
    content = models.TextField()

    def __str__(self):
        return f"{self.author.first_name}: {self.content[:100]}"