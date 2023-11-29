from rest_framework.routers import DefaultRouter

from . import views


app_name = 'posts'

router = DefaultRouter()
router.register('', views.PostViewSet)

urlpatterns = router.urls