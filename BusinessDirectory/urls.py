from django.urls import path
from .views import (
    top_rated_listings, user_listings, Business_listing
)

urlpatterns = [
    path('api/listings/top_rated/', top_rated_listings, name='top-rated'),
    path('api/me/listings/', user_listings, name='user-listings'),
    path('api/listings/<int:pk>/', Business_listing, name='business-listing')
]