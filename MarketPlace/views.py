
from rest_framework import (
    generics, viewsets, decorators, status, permissions
)
from rest_framework.response import Response
from django.db.models import Count
from helpers import pagination
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


class GetCartView(viewsets.GenericViewSet):

    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.PaginatorGenerator()(_page_size=10)

    def get_queryset(self):
        if hasattr(self.request.user, 'cart'):
            return CartItem.objects.filter(cart=self.request.user.cart)
        return []

    def get_serializer_class(self):
        if self.action=='get_user_cart':
            return CartSerializer
        elif self.action=='get_user_cart_items':
            return CartItemSerializer

    @decorators.action(detail=True)
    def get_user_cart(self, request, *args, **kwargs):
        "API Viewset action to get the currently authenticated user's cart"
        cart, created = Cart.objects.get_or_create(owner=request.user)
        serializer = self.get_serializer(cart, many=False)
        data = {**serializer.data, **{'new_cart':created}}
        return Response(data, status=status.HTTP_200_OK)


    @decorators.action(detail=False)
    def get_user_cart_items(self, request, *args, **kwargs):
        "API Viewset action to get the currently authenticated user's cart items"
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
