from django.urls import path
from . import views

urlpatterns = [
    path('mobile/', views.mobile_list, name='mobile_list'),
    path('mobiles/<int:pk>/', views.mobile_detail, name='mobile_detail'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/increase_quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/delete/<int:item_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('checkout/', views.order_create, name='order_create'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_to_wishlist/<str:item_type>/<int:item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('remove_from_wishlist/<str:item_type>/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),


]
