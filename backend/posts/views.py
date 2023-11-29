from rest_framework import viewsets, views, status, permissions
from rest_framework.response import Response

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