from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DirectorViewSet, MovieViewSet, DVDViewSet, OrderViewSet

router = DefaultRouter()
router.register('directors', DirectorViewSet)
router.register('movies', MovieViewSet)
router.register('dvds', DVDViewSet)
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
