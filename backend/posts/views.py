from uuid import UUID

from rest_framework import viewsets, views, status, permissions, mixins, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.request import Request
from rest_framework.authentication import TokenAuthentication

from . import serializers
from . import models
from .permissions import PublicGetPermission


class PostViewSet(viewsets.ModelViewSet):

    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):

        if self.action == 'create' and self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        
        return [permissions.AllowAny()]
    
    @action(detail=True, methods=['POST'])
    def save(self, request, pk=None):
        post = self.get_object()
        models.SavedPost.objects.get_or_create(post=post, user=request.user)
        return Response(status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['GET'])
    def saved(self, request):
        saved_queryset = models.SavedPost.objects.filter(user=request.user).values('post__id')
        posts_queryset = self.get_queryset().filter(id__in=saved_queryset)
        serializer = serializers.PostSerializer(posts_queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


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
    

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([PublicGetPermission])
def comment_reactions_view(request: Request, comment_uuid: UUID):

    comment = models.Comment.objects.get(id=comment_uuid)

    queryset = models.Reaction.objects.filter(comment=comment)
    
    if request.method == 'GET':
        serializer = serializers.ReactionSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        queryset = queryset.filter(user=request.user)
        if queryset.exists():
            reaction = queryset.first()
        else:
            reaction = models.Reaction.objects.create(
                type=request.data,
                user=request.user,
                comment=comment,
            )

        serializer = serializers.ReactionSerializer(reaction)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    if request.method == 'DELETE':

        models.Reaction.objects.filter(user=request.user).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class CommentDetailAPIView(generics.RetrieveAPIView):

    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer


class PostReportsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):

    serializer_class = serializers.ReportSerializer
    queryset = models.Report.objects.all()

    def list(self, request, post, *args, **kwargs):
        self.queryset = self.queryset.filter(post__id=post)
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post_id=self.kwargs['post'])