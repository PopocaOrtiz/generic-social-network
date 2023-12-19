from rest_framework import generics, permissions, authentication

from market import serializers, models


class ProductModelListCreateAPIView(generics.ListCreateAPIView):

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    authentication_classes = [authentication.TokenAuthentication]

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]