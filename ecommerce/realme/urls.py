from django.urls import path
from . import views

urlpatterns = [
    path('mobile/', views.mobile_list, name='mobile_list'),
    path('mobiles/<int:pk>/', views.mobile_detail, name='mobile_detail'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/increase_quantity/<int:item_id>/', views.increase_qunatity, name='increase_quantity'),
    path('cart/decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity')
]