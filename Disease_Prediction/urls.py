from django.urls import path
from . import views

urlpatterns = [
    # path('api/diseases/new/', views.post_disease, name='post_disease'),
    path('api/analyze-disease/', views.analyze_disease, name='analyze-disease'),
]
