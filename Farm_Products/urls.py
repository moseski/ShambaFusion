from django.urls import path
from . import views

urlpatterns = [
    
    path('get_products/', views.get_products, name='get_products'),
    path('get_product/<int:pk>/', views.get_product, name='get_product'),
    path('post_product/', views.post_product, name='post_product'),
    path('update_product/<int:pk>/', views.update_product, name='update_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),


    path('get_categories/', views.get_categories, name='get_categories'),
    path('get_category/<int:pk>/', views.get_category, name='get_category'),
    path('post_category/', views.post_category, name='post_category'),
    path('update_category/<int:pk>/', views.update_category, name='update_category'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),



]    
