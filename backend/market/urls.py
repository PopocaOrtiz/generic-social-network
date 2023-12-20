from django.urls import path

from market import views


app_name = "market"

urlpatterns = [
    path("products/", views.ProductModelListCreateAPIView.as_view(), name="products"),
]