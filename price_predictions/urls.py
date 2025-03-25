from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PricePredictionViewSet

router = DefaultRouter()
router.register(r'predictions', PricePredictionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]