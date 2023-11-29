from rest_framework import viewsets
from rest_framework import permissions

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
