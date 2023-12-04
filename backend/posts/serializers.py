from rest_framework import serializers

from . import models
from users.serializers import UserSerializer
from aws.facades.s3 import S3


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
    image_file = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = models.Post
        fields = ['id', 'author', 'content', 'created_at', 'url', 'image', 'image_file']

    def create(self, validated_data):

        image_file = validated_data.pop('image_file', None)
        post = models.Post.objects.create(
            author=self.context['request'].user,
            **validated_data
        )

        if not image_file:
            return post
    
        url = S3().upload_inmemory_file(image_file, "posts-images")

        post.image = url
        post.save()

        return post


class ReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Reaction
        fields = '__all__'
        read_only_fields = ['id', 'user']