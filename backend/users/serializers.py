from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _

from aws.facades.s3 import S3


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        style={
            'input_type': 'password',
        },
        trim_whitespace=False
    )

    file = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'first_name', 'last_name', 'image', 'file', 'full_name', 'username']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8
            }
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password', None)
        return data
    
    def create(self, validated_data):

        if file := validated_data.pop('file', None):
            url = S3().upload_in_memory_file(file, 'users')
            validated_data['image'] = url

        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        trim_whitespace=False,
    )

    def validate(self, attrs):

        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('Not valid credentials')
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs