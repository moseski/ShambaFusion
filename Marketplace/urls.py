from django.urls import path
from . import views

urlpatterns = [
    # OrderTracking APIs
    path('get_orders/', views.get_orders, name='get_orders'),
    path('get_order/<int:pk>/', views.get_order, name='get_order'),
    path('post_order/', views.post_order, name='post_order'),
    path('update_order/<int:pk>/', views.update_order, name='update_order'),
    path('delete_order/<int:pk>/', views.delete_order, name='delete_order'),

    # CheckOut APIs
    path('get_checkouts/', views.get_checkouts, name='get_checkouts'),
    path('get_checkout/<int:pk>/', views.get_checkout, name='get_checkout'),
    path('post_checkout/', views.post_checkout, name='post_checkout'),
    path('update_checkout/<int:pk>/', views.update_checkout, name='update_checkout'),
    path('delete_checkout/<int:pk>/', views.delete_checkout, name='delete_checkout'),



    path('get_orders/', views.get_orders, name='get_orders'),
    path('get_order/<int:pk>/', views.get_order, name='get_order'),
    path('post_order/', views.post_order, name='post_order'),
    path('update_order/<int:pk>/', views.update_order, name='update_order'),
    path('delete_order/<int:pk>/', views.delete_order, name='delete_order'),
]