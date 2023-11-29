
from django.urls import re_path, path
from .views import *

app_name = 'MarketPlace'
urlpatterns = [
    re_path(
        '^marketplace/all/?$',
        GetAllMarketPlacesView.as_view(),
        name='marketplaces-list'
    ),
    re_path(
        '^marketplace/(?P<pk>\d+)/products/categories/?$',
        GetProductCategoriesView.as_view({'get':'get_all_categories'}),
        name='marketplace-product-categories-list'
    ),
    re_path(
        '^marketplace/(?P<pk>\d+)/products/categories/popular/?$',
        GetProductCategoriesView.as_view({'get':'get_popular_categories'}),
        name='marketplace-popular-product-categories-list'
    ),
    re_path(
        '^me/cart/?$',
        GetCartView.as_view({'get':'get_user_cart'}),
        name='user-cart-detail'
    ),
    path('me/orders/', UserOrderListView.as_view(), name='user_order_list'),
    path('me/orders/create/', CreateOrderView.as_view(), name='create_order'),
    path('me/orders/<int:pk>/', UpdateOrderView.as_view(), name='update_order'),
    path('me/orders/<int:pk>/cancel/', CancelOrderView.as_view(), name='cancel_order'),
]
