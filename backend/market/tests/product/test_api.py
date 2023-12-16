import pytest
from posts.models import Product
from rest_framework import status


@pytest.fixture
def create_product():
    product = Product.objects.create(name="Test Product", price=10.99)
    yield product
    product.delete()


@pytest.mark.django_db
@pytest.mark.xfail
def test_fetch_product_list(auth_client, create_product):
    client, user = auth_client()
    url = reverse("market:products")
    response = client.get(url)
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == 3


@pytest.mark.django_db
@pytest.mark.xfail
def test_create_product_list(auth_client):
    client, user = auth_client()
    url = reverse("market:products")
    data = {
        "name": "New Product",
        "price": 19.99
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
