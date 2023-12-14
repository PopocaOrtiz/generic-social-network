import pytest
from django.urls import reverse
from rest_framework import status

from users import models, serializers
from users.tests import conftest


@pytest.mark.xfail
@pytest.mark.django_db
def test_get_following(auth_client, create_user: conftest.CreateUserFixture):

    ME_FOLLOWING_URL = reverse('users:me-following')
    
    client, follower = auth_client()

    followed1 = create_user()
    followed2 = create_user()

    models.Follow.objects.create(follower=follower, followed=followed1)
    models.Follow.objects.create(follower=follower, followed=followed2)

    followeds = models.Follow.objects.filter(follower=follower)
    serializer = serializers.UserSerializer(data=followeds, many=True)

    res = client.get(ME_FOLLOWING_URL)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data