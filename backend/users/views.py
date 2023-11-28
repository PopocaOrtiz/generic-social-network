from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from . import serializers


class UserViewSet(viewsets.ModelViewSet):

    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer


class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer