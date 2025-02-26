from django.urls import path
from . import views

urlpatterns = [
    path('api/insights/', views.get_insights, name='get_insights'),
]
