from django.urls import path, include
from rest_framework import routers

from jobs import views


app_name = 'jobs'


router = routers.DefaultRouter()
router.register(r'', views.JobListApiView, basename='jobs')


urlpatterns = [
    path('', include(router.urls)),
]