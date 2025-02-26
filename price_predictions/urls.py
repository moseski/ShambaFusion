from django.urls import path
from . import views

urlpatterns = [
    path('api/market-data/', views.market_data_view, name='market_data'),
    path('api/market-data/<int:pk>/', views.market_data_detail_view, name='market_data_detail'),
    path('api/price-predictions/', views.price_prediction_view, name='price_predictions'),
    path('api/price-predictions/<int:pk>/', views.price_prediction_detail_view, name='price_prediction_detail'),
]
