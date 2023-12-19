from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import permissions, authentication
from django.db.models import Q, Max, F

from chat import models, serializers


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([authentication.TokenAuthentication])
def conversations_list(request):

    user = request.user

    conversations = (models.Message.objects
        .filter(Q(sender=user) | Q(receiver=user))
        .values('receiver', receiver_name=F('receiver__first_name'))
        .annotate(
            latest_message=Max('message'),
            latest_message_date=Max('created_at')
        )
        .order_by('-latest_message_date')
    )

    serializer = serializers.ConversationSerializer(conversations, many=True)
    
    return Response(serializer.data)