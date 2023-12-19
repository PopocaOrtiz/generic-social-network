from rest_framework import viewsets, mixins, permissions, authentication

from jobs import models, serializers


class JobListApiView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):

    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer
    authentication_classes = [authentication.TokenAuthentication]

    def get_permissions(self):

        if self.action == 'list':
            return [permissions.AllowAny()]
        
        return [permissions.IsAuthenticated()]