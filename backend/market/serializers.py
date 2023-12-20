from rest_framework import serializers

from market.models import Product


class ProductSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Product
        fields = "__all__"