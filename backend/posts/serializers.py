from rest_framework import serializers

from . import models
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    author = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = '__all__'

    def get_comments(self, obj):
        comments = models.Comment.objects.filter(comment=obj)
        serializer = self.__class__(comments, many=True, context=self.context)
        return serializer.data


class PostSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    author = UserSerializer(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='posts:post-detail',
        lookup_field='pk',
    )

    class Meta:
        model = models.Post
        fields = ['id', 'author', 'content', 'created_at', 'url', 'image']


class ReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Reaction
        fields = '__all__'
        read_only_fields = ['id', 'user']