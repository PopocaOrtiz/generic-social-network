from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'posts'

router = DefaultRouter()
router.register(r'', views.PostViewSet)

reactions_router = DefaultRouter()
reactions_router.register('', views.ReactionViewSet)


"""
path('posts/')       t                     ok  root
path('posts/<uuid:id>')                    ok
path('posts/<uuid:id>/comments/')          ok
path('posts/<uuid:id>/reactions/')         ok

path('posts/comments/')                    __  unnecesary
path('posts/comments/<uuid:id>')           __
path('posts/comments/<uuid:id>/comments')  __
path('posts/comments/<uuid:id>/reactions') ok
"""

urlpatterns = [
    path('', include(router.urls)),
    path('<uuid:post>/comments/', views.CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comments'),
    path('<uuid:post>/reactions/', include(reactions_router.urls)),

    path('comments/<uuid:pk>', views.CommentDetailAPIView.as_view(), name='comment-detail'),
    # path('comments/<uuid:comment>/comments/', views, name='comment-comments'),
    path('comments/<uuid:comment_uuid>/reactions/', views.comment_reactions_view, name='comment-reactions'),
]