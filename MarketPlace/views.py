
from rest_framework import generics, status, permissions, pagination
from rest_framework.response import Response
from .serializers import *
from .models import *


class GetAllMarketPlacesView(generics.GenericAPIView):

    "API View to get all marketplaces"

    queryset = MarketPlace.objects.order_by('-id')
    permission_classes = [permissions.AllowAny]
    serializer_class = MarketPlaceSerializer


    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllProductCategoriesView(generics.GenericAPIView):

    "API View to get all product categories within a marketplace"

    queryset = MarketPlace.objects.order_by('-id')
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductCategorySerializer

    def get(self, request, *args, **kwargs):
        marketplace = self.get_object()
        product_categories = marketplace.product_categories.all()
        serializer = self.get_serializer(product_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
