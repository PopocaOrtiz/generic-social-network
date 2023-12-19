from rest_framework import serializers


class ConversationSerializer(serializers.Serializer):

    receiver_name = serializers.CharField()
    latest_message = serializers.CharField()
    latest_message_date = serializers.DateTimeField()