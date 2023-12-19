import uuid

from django.db import models
from django.contrib.auth import get_user_model


class Product(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.name