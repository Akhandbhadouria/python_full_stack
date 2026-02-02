from django.urls import path
from . import views

urlpatterns = [
    path('product/<int:pk>/', views.product_detail, name="st_detail"),
    path('data_input/', views.data_input, name='data_input'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('orders/', views.order_list, name='order_list'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('all-orders/', views.all_orders, name='all_orders'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
]