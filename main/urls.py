from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import *


router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('ratings', RatingViewSet)
router.register('likes', LikeViewSet)
router.register('comments', CommentViewSet)
router.register('favorites', FavoritesViewSet)


urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('search/', SearchListView.as_view()),
    path('', include(router.urls)),
]