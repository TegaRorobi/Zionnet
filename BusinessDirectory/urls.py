from django.urls import path
from .views import BusinessListingListCreateView

urlpatterns = [
    path('listings/', BusinessListingListCreateView.as_view(), name='business-listings'),
]
