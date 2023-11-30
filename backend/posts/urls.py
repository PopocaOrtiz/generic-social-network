from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'posts'

router = DefaultRouter()
router.register(r'', views.PostViewSet)

reactions_router = DefaultRouter()
reactions_router.register('', views.ReactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('<uuid:post>/comments/', views.CommentView.as_view()),
    path('<uuid:post>/comments/', views.CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comments'),
    path('<uuid:post>/reactions/', include(reactions_router.urls))
]