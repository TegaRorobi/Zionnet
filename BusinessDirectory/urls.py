from django.urls import path
from .views import (
    BusinessListingCategoryListView,
    BusinessListingListCreateView,
    PopularBusinessListingCategoryListView,
)

urlpatterns = [
    path(
        "listings/", BusinessListingListCreateView.as_view(), name="business-listings"
    ),
    path(
        "categories/",
        BusinessListingCategoryListView.as_view(),
        name="business-categories",
    ),
    path(
        "categories/popular/",
        PopularBusinessListingCategoryListView.as_view(),
        name="popular-category-list",
    ),
]
