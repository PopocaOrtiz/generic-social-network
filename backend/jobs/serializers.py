from rest_framework import serializers

from jobs import models
from users.serializers import UserSerializer


class JobSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = models.Job
        fields = "__all__"

    def create(self, validated_data):

        validated_data["user"] = self.context["request"].user

        return super().create(validated_data)