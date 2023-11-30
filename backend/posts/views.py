from rest_framework import viewsets, views, status, permissions, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view

from . import serializers
from . import models


class PostViewSet(viewsets.ModelViewSet):

    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):

        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        
        return super().get_permissions()


class CommentView(views.APIView):

    serializer_class = serializers.CommentSerializer

    def get(self, request, post):

        comments = []
        for comment in models.Comment.objects.filter(post=post):
            comments.append({
                'id': comment.id,
                'author': comment.author, 
                'content': comment.content,
                'post': comment.post
            })

        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, post):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            
            comment = models.Comment.objects.create(
                author=self.request.user,
                **serializer.validated_data
            )

            return Response(
                self.serializer_class(comment).data, 
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()

    def list(self, request, post, *args, **kwargs):
        self.queryset = self.queryset.filter(post=post)
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):

        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        
        return super().get_permissions()
    

class ReactionViewSet(
        mixins.ListModelMixin, 
        mixins.CreateModelMixin, 
        mixins.DestroyModelMixin, 
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet,
    ):

    queryset = models.Reaction.objects.all()
    serializer_class = serializers.ReactionSerializer

    def list(self, request, post):
        self.queryset = self.queryset.filter(post=post)
        return super().list(request)

    def create(self, request, post, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        reaction: models.Reaction = self.queryset.filter(post__id=post).exists()  # type: ignore

        if not reaction:
            serializer.save(
                user=self.request.user,
                post_id=post
            )

        reaction: models.Reaction = self.queryset.get(post__id=post)  # type: ignore

        reaction.refresh_from_db()
        serializer = self.serializer_class(reaction)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_permissions(self):

        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        
        return []
    

@api_view()
def comment_reactions_view(request, post_uuid, comment_uuid):

    models.Post.objects.get(id=post_uuid)
    comment = models.Comment.objects.get(id=comment_uuid)
    
    if request.method == 'GET':
        reactions = models.Reaction.objects.filter(comment=comment)
        serializer = serializers.ReactionSerializer(reactions, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)