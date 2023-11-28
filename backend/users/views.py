from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model

from . import serializers


class CreateUserView(generics.CreateAPIView):

    queryset = get_user_model().objects.none()
    serializer_class = serializers.UserSerializer


class CreateTokenView(ObtainAuthToken):

    serializer_class = serializers.AuthTokenSerializer