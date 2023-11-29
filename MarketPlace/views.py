
from rest_framework import (
    generics, viewsets, decorators, status, permissions
)
from rest_framework.response import Response
from django.db.models import Count
from .serializers import *
from .models import *
from .permissions import IsOrderOwner



class GetAllMarketPlacesView(generics.GenericAPIView):

    "API View to get all marketplaces"

    queryset = MarketPlace.objects.order_by('-id')
    permission_classes = [permissions.AllowAny]
    serializer_class = MarketPlaceSerializer


    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetProductCategoriesView(viewsets.GenericViewSet):

    "API View to get product categories within a marketplace"

    queryset = MarketPlace.objects.order_by('-id')
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductCategorySerializer

    @decorators.action(detail=False)
    def get_all_categories(self, request, *args, **kwargs):
        "API Viewset action to get all product categories within a marketplace"
        try:
            marketplace = self.get_object()
        except:
            return Response({
                'error': f'MarketPlace with {self.lookup_field} '
                f'{kwargs[self.lookup_url_kwarg or self.lookup_field]} does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
        product_categories = marketplace.product_categories.order_by('name')
        serializer = self.get_serializer(product_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @decorators.action(detail=False)
    def get_popular_categories(self, request, *args, **kwargs):
        "API Viewset action to get popular product categories within a marketplace"
        try:
            marketplace = self.get_object()
        except:
            return Response({
                'error': f'MarketPlace with {self.lookup_field} '
                f'{kwargs[self.lookup_url_kwarg or self.lookup_field]} does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
        product_categories = marketplace.product_categories.annotate(
            product_count=Count('products')
        ).order_by('-product_count')
        serializer = self.get_serializer(product_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)

class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

class UpdateOrderView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOrderOwner]

class CancelOrderView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOrderOwner]
