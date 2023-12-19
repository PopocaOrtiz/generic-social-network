import uuid

from django.db import models


class Ad(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    creator = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by {self.creator.full_name}"