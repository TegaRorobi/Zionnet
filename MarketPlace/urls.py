
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
        CartView.as_view({'get':'get_user_cart'}),
        name='user-cart-detail'
    ),
    re_path(
        '^me/cart/items/?$',
        CartView.as_view({'get':'get_user_cart_items'}),
        name='user-cart-items-list'
    ),
    re_path(
        '^me/cart/dump/?$',
        CartView.as_view({'delete':'delete_user_cart_items'}),
        name='user-cart-dump'
    ),
    re_path(
        '^stores/vendor/request/?$',
        StoreVendorView.as_view({'post':'create_store_vendor_request'}),
        name='store-vendor-request-create'
    ),
    re_path(
        '^me/stores/?$',
        StoreView.as_view(
            {
                'get':'get_user_stores',
                'post':'create_store',
            }
        ),
        name='store-list-create'
    ),
    re_path(
        '^me/stores/(?P<pk>\d+)/?$',
        StoreView.as_view(
            {
                'get':'retrieve_store',
                'put':'update_store',
                'patch':'partial_update_store',
                'delete':'destroy_store'
            }
        ),
        name='store-retrieve-update-delete'
    ),
    path('me/orders/', UserOrderListView.as_view(), name='user_order_list'),
    path('me/orders/create/', CreateOrderView.as_view(), name='create_order'),
    path('me/orders/<int:pk>/', UpdateOrderView.as_view(), name='update_order'),
    path('me/orders/<int:pk>/cancel/', CancelOrderView.as_view(), name='cancel_order'),
]
