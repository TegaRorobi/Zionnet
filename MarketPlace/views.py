
from rest_framework import (
    generics, viewsets, mixins, decorators, status, permissions
)
from .permissions import IsApprovedStoreVendor
from rest_framework.response import Response
from django.db.models import Count,Avg
from helpers import pagination
from .serializers import *
from .models import *
from .permissions import IsOrderOwner, IsStoreOwner
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone



class GetAllMarketPlacesView(generics.GenericAPIView):

    "API View to get all marketplaces"

    queryset = MarketPlace.objects.order_by('-id')
    permission_classes = [permissions.AllowAny]
    serializer_class = MarketPlaceSerializer


    @swagger_auto_schema(tags=['MarketPlace'])
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
    @swagger_auto_schema(tags=['MarketPlace - Products'])
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
    @swagger_auto_schema(tags=['MarketPlace - Products'])
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
    @swagger_auto_schema(tags=['MarketPlace - Cart'])
    def get_user_cart(self, request, *args, **kwargs):
        "API Viewset action to get the currently authenticated user's cart"
        cart, created = Cart.objects.get_or_create(owner=request.user)
        serializer = self.get_serializer(cart, many=False)
        data = {**serializer.data, **{'new_cart':created}}
        return Response(data, status=status.HTTP_200_OK)


    @decorators.action(detail=False)
    @swagger_auto_schema(tags=['MarketPlace - Cart'])
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
    @swagger_auto_schema(tags=['MarketPlace - Cart'])
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
    @swagger_auto_schema(tags=['MarketPlace - Stores'])
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
    @swagger_auto_schema(tags=['MarketPlace - Stores'])
    def get_user_stores(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.action(detail=True)
    @swagger_auto_schema(tags=['MarketPlace - Stores'])
    def create_store(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(vendor=request.user.store_vendor_profile)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(detail=True)
    @swagger_auto_schema(tags=['MarketPlace - Stores'])
    def retrieve_store(self, request, *args, **kwargs):
        store = self.get_object()
        serializer = self.get_serializer(store, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.action(detail=True)
    @swagger_auto_schema(tags=['MarketPlace - Stores'])
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
    @swagger_auto_schema(tags=['MarketPlace - Stores'])
    def partial_update_store(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update_store(request, *args, **kwargs)

    @decorators.action(detail=True)
    @swagger_auto_schema(tags=['MarketPlace - Stores'])
    def destroy_store(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response(
            {'message': 'Store successfully deleted.'}, 
            status=status.HTTP_204_NO_CONTENT
        )


class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    @swagger_auto_schema(tags=['MarketPlace - Orders'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)


class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    @swagger_auto_schema(tags=['MarketPlace - Orders'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)


class UpdateOrderView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOrderOwner]

    @swagger_auto_schema(tags=['MarketPlace - Orders'])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=['MarketPlace - Orders'])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

class CancelOrderView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOrderOwner]

    @swagger_auto_schema(tags=['MarketPlace - Orders'])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class StoreProductListCreateView(generics.ListCreateAPIView):
    """API endpoint for CRUD operations for products within a store"""

    serializer_class = ProductSerializer
    permission_classes = [IsStoreOwner]

    def get_queryset(self):
        """API endpoint to retrieve all products within a store"""
        store_id = self.kwargs["store_id"]

        return Product.objects.filter(store__id=store_id)

    def perform_create(self, serializer):
        store_id = self.kwargs["store_id"]
        store = get_object_or_404(Store, id=store_id)

        serializer.is_valid(raise_exception=True)
        product = serializer.save(store=store)

    @swagger_auto_schema(tags=['MarketPlace - Products'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=['MarketPlace - Products'])
    def post(self, request, *args, **kwargs):
        """API endpoint to create product within a store"""
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class StoreProductUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsStoreOwner]

    @swagger_auto_schema(tags=['MarketPlace - Products'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=['MarketPlace - Products'])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=['MarketPlace - Products'])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=['MarketPlace - Products'])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        store_id = self.kwargs["store_id"]
        product_id = self.kwargs["pk"]

        return Product.objects.filter(id=product_id, store__id=store_id)


class GetPopularProductsView(generics.ListAPIView):
    "API View to get all popular products  within a marketplace"
    serializer_class = ProductSerializer

    def get_queryset(self):
        market_id = self.kwargs.get('pk')

        # Retrieve the market place based on the provided id
        try:
            market = MarketPlace.objects.get(pk=market_id)
        except MarketPlace.DoesNotExist:
            raise MarketPlace.DoesNotExist("MarketPlace not found.")

        # Get all products associated with the market place
        products = Product.objects.filter(store__marketplace=market)
       


        # Calculate product popularity based on ratings
        # Filter out products with an average rating of 3.5 or above
        popular_products = products.annotate(
            average_rating=Avg('ratings__value')
        ).filter(average_rating__gte=3.5)

        # Return the sorted list of popular products
        return popular_products
    
    @swagger_auto_schema(tags=['MarketPlace - Products'])
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        # Check if any popular products were found
        try:
            queryset = self.get_queryset()

            if queryset:
                # Return the sorted list of popular products
               serialized_products = self.serializer_class(queryset, many=True)
               return Response(serialized_products.data, status=status.HTTP_200_OK)
            else:
                return Response({
                'error': f'Popular products for MarketPlace with {self.lookup_field} '
                f'{kwargs[self.lookup_url_kwarg or self.lookup_field]} does not exist'
            }, status=status.HTTP_404_NOT_FOUND)

        except MarketPlace.DoesNotExist:
            # Handle the exception and return a specific error response
            return Response({
                'error': f'MarketPlace with {self.lookup_field} '
                f'{kwargs[self.lookup_url_kwarg or self.lookup_field]} does not exist'
            }, status=status.HTTP_404_NOT_FOUND)


class HotDealsView(generics.ListAPIView):
    "API View to get hot deals products  within a marketplace "
    serializer_class = ProductSerializer

    def get_queryset(self):
        market_id = self.kwargs.get('pk')

        # Retrieve the market place based on the provided id
        try:
            market = MarketPlace.objects.get(pk=market_id)
        except MarketPlace.DoesNotExist:
            raise MarketPlace.DoesNotExist("MarketPlace not found.")

        # Get all products associated with the market place and have discount greater than 50%
        hot_deals = Product.objects.filter(store__marketplace=market, discount__gte=50)
        
        return hot_deals
    
    @swagger_auto_schema(tags=['MarketPlace - Products'])
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        # Check if any hot deals were found
        try:
            queryset = self.get_queryset()

            if queryset:
                # Return the sorted list of hot deals
                serialized_hot_deals = self.serializer_class(queryset, many=True)
                return Response(serialized_hot_deals.data, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': f'Hot deals for MarketPlace with {self.lookup_field} '
                             f'{kwargs[self.lookup_url_kwarg or self.lookup_field]} do not exist'
                }, status=status.HTTP_404_NOT_FOUND)

        except MarketPlace.DoesNotExist:
            # Handle the exception when market doesn't exist 
            return Response({
                'error': f'MarketPlace with {self.lookup_field} '
                         f'{kwargs[self.lookup_url_kwarg or self.lookup_field]} does not exist'
            }, status=status.HTTP_404_NOT_FOUND)


class FlashSaleProductsView(generics.ListAPIView):
    "API View to get all  products on flash sales within a marketplace"
    serializer_class = FlashSaleSerializer

    def get_queryset(self):
        market_id = self.kwargs.get('pk')

        # Retrieve the market place based on the provided id
        try:
            market = MarketPlace.objects.get(pk=market_id)
        except MarketPlace.DoesNotExist:
            raise MarketPlace.DoesNotExist("MarketPlace not found.")

        # Get all flash sales associated with the market place
        now = timezone.now()
        flash_sales = FlashSale.objects.filter(
            product__store__marketplace=market,
            start_datetime__lte=now,
            end_datetime__gte=now
        )

        return flash_sales
    
    @swagger_auto_schema(tags=['MarketPlace - Products'])
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def list(self, request, *args, **kwargs):
      # Check if any hot deals were found
        try:
            queryset = self.get_queryset()

            if queryset.exists():
                serialized_flash_sales = self.serializer_class(queryset, many=True)
                return Response(serialized_flash_sales.data, status=status.HTTP_200_OK)
            else:
                return Response(
                  {'error': f'No flash sales found for products of MarketPlace with {self.lookup_field} 'f'{kwargs[self.lookup_url_kwarg or self.lookup_field]} exist'
                },
                status=status.HTTP_404_NOT_FOUND
            )
  
        except MarketPlace.DoesNotExist:
            # Handle the exception when market doesn't exist 
            return Response({
                'error': f'MarketPlace with {self.lookup_field} '
                         f'{kwargs[self.lookup_url_kwarg or self.lookup_field]} does not exist'
            }, status=status.HTTP_404_NOT_FOUND)


class CreateFlashSaleView(generics.CreateAPIView):
    "API View to get all popular products  within a marketplace"
    serializer_class = FlashSaleSerializer
    # permission_classes = [permissions.AllowAny]  # You can adjust permissions as needed

    def get_queryset(self):
        market_id = self.kwargs.get('pk', None)
        product_id = self.kwargs.get('product_id', None)

        # Retrieve the market place based on the provided id
        try:
            market = MarketPlace.objects.get(pk=market_id)
        except MarketPlace.DoesNotExist:
            raise MarketPlace.DoesNotExist(f'MarketPlace with {self.lookup_field}'   f' {self.kwargs[self.lookup_url_kwarg or self.lookup_field]} does not exist')

        # Get the product associated with the market place
        try:
            product = Product.objects.get(store__marketplace=market,
            pk=product_id)
            return product
        except Product.DoesNotExist:
            return None

    @swagger_auto_schema(tags=['MarketPlace - Products'])
    def post(self, request, *args, **kwargs):
        try:
            product = self.get_queryset()

            if not product:
                return Response({
                    'error':f'Product of pk {kwargs.get("product_id")} for MarketPlace with {self.lookup_field} {self.kwargs[self.lookup_url_kwarg or self.lookup_field]} does not exist'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Check if a flash sale already exists for the product
            if FlashSale.objects.filter(product=product).exists():
                return Response({
                    'error': 'Flash sale already exists for this product'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Perform create if everything is valid
            serializer.save(product=product)  # Added saving the product

            return Response({
                'success': 'Flash sale created successfully',
                'data': serializer.data
                
            }, status=status.HTTP_201_CREATED)

        except MarketPlace.DoesNotExist as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_404_NOT_FOUND)
            