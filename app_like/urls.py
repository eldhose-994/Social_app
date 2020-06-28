from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from app_like.views import PostViewSet, ReactionPostView

router = routers.DefaultRouter()
router.register(r'post', PostViewSet, basename='post')
router.register(r'react', ReactionPostView, basename='reacting_post')

urlpatterns = [
    path('', include(router.urls)),
]
#
# urlpatterns = [
#     path('', views.index, name='index'),
# ]/
