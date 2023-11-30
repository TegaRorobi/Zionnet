from django.urls import re_path, path
from .views import *

app_name = "MarketPlace"
urlpatterns = [
    re_path(
        "^marketplace/all/?$",
        GetAllMarketPlacesView.as_view(),
        name="marketplaces-list",
    ),
    re_path(
        "^marketplace/(?P<pk>\d+)/products/categories/?$",
        GetProductCategoriesView.as_view({"get": "get_all_categories"}),
        name="marketplace-product-categories-list",
    ),
    re_path(
        "^marketplace/(?P<pk>\d+)/products/categories/popular/?$",
        GetProductCategoriesView.as_view({"get": "get_popular_categories"}),
        name="marketplace-popular-product-categories-list",
    ),
    re_path(
        "^me/cart/?$",
        GetCartView.as_view({"get": "get_user_cart"}),
        name="user-cart-detail",
    ),
    re_path(
        "^me/cart/items/?$",
        GetCartView.as_view({"get": "get_user_cart_items"}),
        name="user-cart-items-list",
    ),
    path(
        "me/stores/<int:store_id>/products/",
        StoreProductListCreateView.as_view(),
        name="store-products",
    ),
    path(
        "me/stores/<int:store_id>/products/<int:product_id>",
        StoreProductUpdateView.as_view(),
        name="store-product",
    ),
]
