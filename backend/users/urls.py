from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'users'

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls))
]