from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profile', ProfileViewset)
# router.register(r'products', ProductViewSet)
# router.register(r'diseases', DiseaseViewSet)
# router.register(r'insights', FarmInsightsViewSet)
# router.register(r'order', OrderTrackingViewSet)
# router.register(r'checkout', CheckoutViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    # path('api/predict-treatment/', DiseasePredictionView.as_view(), name='predict-treatment'),
]