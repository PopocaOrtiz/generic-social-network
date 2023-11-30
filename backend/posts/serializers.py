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
    url = serializers.HyperlinkedIdentityField(
        view_name='posts:post-detail',
        lookup_field='pk',
    )

    class Meta:
        model = models.Post
        fields = ['id', 'author', 'content', 'created_at', 'url']


class ReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Reaction
        fields = '__all__'
        read_only_fields = ['id', 'user']