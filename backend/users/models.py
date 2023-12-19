import uuid
from typing import Type

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if 'username' not in extra_fields:
            extra_fields['username'] = ''

        user = get_user_model().objects.create(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True  # type: ignore
        user.is_superuser = True  # type: ignore
        user.save()
        return user


class User(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    image = models.URLField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

UserType = Type[User]


class Group(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name
    

class Follow(models.Model):
    follower = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower', 'followed')

    def save(self, *args, **kwargs):

        if self.follower == self.followed:
            raise ValidationError('user cannot follow himself')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.follower.id} follows {self.followed.id}"  # type: ignore