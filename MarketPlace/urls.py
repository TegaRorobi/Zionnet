
from django.urls import re_path
from .views import *

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
    )
]