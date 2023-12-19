import uuid

from django.db import models
from django.contrib.auth import get_user_model


class Message(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField()
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="messages_sended")
    receiver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="messages_received")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"