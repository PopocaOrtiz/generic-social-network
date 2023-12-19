import pytest
from rest_framework import status
from django.urls import reverse

from market.models import Product


@pytest.fixture
def create_product(create_user):
    
    def _create_product(user=None):

        if user is None:
            user = create_user()

        product = Product.objects.create(
            user=user, 
            title="Test Product", 
            description="This is a test product"
        )

        return product
    
    return _create_product


@pytest.mark.django_db
def test_fetch_product_list(api_client, create_product):

    for _ in range(3):
        create_product()

    url = reverse("market:products")
    
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3


@pytest.mark.django_db
def test_create_product_list(auth_client):

    client, _ = auth_client()

    url = reverse("market:products")

    data = {
        "title": "New Product",
        "price": 19.99
    }

    response = client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['title'] == data['title']