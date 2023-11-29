from rest_framework import viewsets

from . import serializers
from . import models


class PostViewSet(viewsets.ModelViewSet):

    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer