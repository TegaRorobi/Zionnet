from django.urls import path
from .views import (
    TopRatedListingsView, UserListingsView, ListingDetailView
)

urlpatterns = [
    path('api/listings/top_rated/', TopRatedListingsView.as_view(), name='top-rated-listings'),
    path('api/me/listings/', UserListingsView.as_view(), name='user-listings'),
    path('api/listings/<int:pk>/', ListingDetailView.as_view(), name='business-listing')
]