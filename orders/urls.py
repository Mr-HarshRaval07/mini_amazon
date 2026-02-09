from django.urls import path
from .views import (
    add_to_cart,
    view_cart,
    checkout,
    my_orders,
    order_detail,
    update_cart,
    payment_view,
    qr_summary
)

urlpatterns = [

    # CART
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),

    # UPDATE CART
    path('update/<int:item_id>/<str:action>/', update_cart, name='update_cart'),

    # CHECKOUT
    path('checkout/', checkout, name='checkout'),

    # PAYMENT
    path("payment/<int:order_id>/", payment_view, name="payment"),
    path("payment/qr/<int:order_id>/", qr_summary, name="qr_summary"),

    # ORDERS
    path('my-orders/', my_orders, name='my_orders'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
]
