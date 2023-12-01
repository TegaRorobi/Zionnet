
from rest_framework import (
    generics, viewsets, mixins, decorators, status, permissions
)
from .permissions import IsApprovedStoreVendor
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


class CartView(viewsets.GenericViewSet):

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
    

    @decorators.action(detail=False)
    def delete_user_cart_items(self, request, *args, **kwargs):
        "API Viewset action to delete the currently authenticated user's cart items"
        queryset = self.filter_queryset(self.get_queryset())
        for cartitem in queryset:
            cartitem.delete()
        return Response({
            "message":"Cart successfully cleared."
        }, status=status.HTTP_204_NO_CONTENT)


class StoreVendorView(viewsets.GenericViewSet, mixins.CreateModelMixin):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StoreVendorSerializer

    @decorators.action(detail=True)
    def create_store_vendor_request(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, is_approved=False)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoreView(viewsets.GenericViewSet, mixins.CreateModelMixin):

    "API Viewset to perform CRUD operations on the store(s) of the currently authenticated user"

    permission_classes = [IsApprovedStoreVendor]
    serializer_class = StoreSerializer

    def get_queryset(self):
        return Store.objects.filter(
            vendor=self.request.user.store_vendor_profile
        )

    @decorators.action(detail=False)
    def get_user_stores(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.action(detail=True)
    def create_store(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(vendor=request.user.store_vendor_profile)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(detail=True)
    def retrieve_store(self, request, *args, **kwargs):
        store = self.get_object()
        serializer = self.get_serializer(store, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.action(detail=True)
    def update_store(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        store = self.get_object()
        serializer = self.get_serializer(store, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            if getattr(store, '_prefetched_objects_cache', None):
                store._prefetched_objects_cache = {}
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(detail=True)
    def partial_update_store(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update_store(request, *args, **kwargs)