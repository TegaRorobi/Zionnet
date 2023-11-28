
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
        GetAllProductCategoriesView.as_view(),
        name='marketplace-product-categories-list'
    )
]