
from django.urls import re_path
from .views import *

urlpatterns = [
    re_path('^marketplace/all/?$', GetAllMarketPlacesView.as_view(), name='marketplaces-list')
]