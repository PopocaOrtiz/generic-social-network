from rest_framework import serializers

from . import models
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = '__all__'



class PostSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = models.Post
        fields = '__all__'