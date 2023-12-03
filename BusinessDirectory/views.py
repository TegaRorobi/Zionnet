from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import Http404
from rest_framework import status, viewsets
from django.db import models
from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsVendorVerified
from django.db.models import Count
from .pagination import ListingPagination
from .serializers import *
from .models import *
from drf_yasg.utils import swagger_auto_schema
from .permissions import IsVendorVerified
from django.db.models import Count, Avg


#endpoint to Retrieve top-rated listings based on average rating
class BusinessListingRatingViewSet(viewsets.ModelViewSet):
    queryset = BusinessListingRating.objects.all()
    serializer_class = BusinessListingRatingSerializer
    permission_classes = []

    @action(detail=False, methods=['GET'])
    def top_rated(self, request):
        try:
            #Get top 5 listings based on average rating
            top_listings = BusinessListingRating.objects.values('listing_id') \
                .annotate(avg_rating=models.Avg('value')) \
                .order_by('-avg_rating')[:5]

            if not top_listings:
                return Response({"error": "No top-rated listings found"}, status=status.HTTP_404_NOT_FOUND)

            listing_ids = [item['listing_id'] for item in top_listings]
            top_listings_data = BusinessListingRating.objects.filter(listing_id__in=listing_ids)

            serializer = self.get_serializer(top_listings_data, many=True)
            return Response(serializer.data)

        except Exception as e:
            error_message = str(e)
            response = {
                'status_message': 'error',
                'message': 'An error occurred: ' + error_message,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#Endpoint to Retrieve user listings
class UserListingsView(generics.ListAPIView):
    serializer_class = BusinessListingSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = []

    def get_queryset(self):
        try:
            return BusinessListing.objects.filter(vendor_id=self.request.user.id)
        except Exception as e:
            raise Exception(str(e))
        
    
#endpoint to get a specific business listing
class ListingDetailView(generics.RetrieveAPIView):
    permission_classes = []
    queryset = BusinessListing.objects.all()
    serializer_class = BusinessListingSerializer

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return Response({"error": "Listing not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            error_message = str(e)
            response = {
                'status_message': 'error',
                'message': 'An error occurred: ' + error_message,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class BusinessListingRequestCreateView(generics.CreateAPIView):
    queryset = BusinessListingRequest.objects.all()
    serializer_class = BusinessListingRequestSerializer

    @swagger_auto_schema(tags=['BusinessDirectory'])
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)


class BusinessListingVendorRequestCreateView(generics.CreateAPIView):
    serializer_class = BusinessListingVendorSerializer

    @swagger_auto_schema(tags=['BusinessDirectory'])
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_approved=False)


class BusinessListingListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating business listings.
    - GET method: Retrieves a paginated list of business listings.
    - POST method: Creates a new business listing along with associated images and files.
    Requires authentication for GET requests. For POST requests,a vendor profile
    verification is required.
    """

    queryset = BusinessListing.objects.all()
    serializer_class = BusinessListingSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "name",
        "description",
        "city",
        "province",
        "country",
        "phone_number",
    ]
    ordering_fields = ["name", "created_at"]
    ordering = ["-created_at"]
    pagination_class = ListingPagination
    permission_classes = [IsVendorVerified]

    @swagger_auto_schema(tags=['BusinessDirectory'])
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


    def retrieve(self, request, *args, **kwargs):
        # retrieves an instance of a listing and attach the related images for the listing
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        images = BusinessListingImage.objects.filter(listing=instance)
        image_serializer = BusinessListingImageSerializer(images, many=True)
        response_data = serializer.data
        response_data["images"] = image_serializer.data

        return Response(response_data)

    def list(self, request, *args, **kwargs):
        # getting list of listings for an authenticated get request with paginated response
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        Custom method to handle the creation of business listings.
        Args:
            serializer: BusinessListingSerializer instance, responsible for validating and saving the main listing details.
        Raises:
            rest_framework.exceptions.ValidationError: If validation fails for the main listing details.
        Creates a new BusinessListing and associates images and files with it.
        """
        images_data = self.request.FILES.getlist("images", [])
        files_data = self.request.FILES.getlist("files", [])

        # Save associated images
        for image_data in images_data:
            image_serializer = BusinessListingImageSerializer(
                data={"image": image_data, "listing": business_listing.id}
            )
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save()

        # save associated files
        for file_data in files_data:
            file_serializer = BusinessListingFileSerializer(
                data={"file": file_data, "listing": business_listing.id}
            )
            file_serializer.is_valid(raise_exception=True)
            file_serializer.save()

        # save an instance of business listing
        serializer.is_valid(raise_exception=True)
        business_listing = serializer.save(vendor_id=self.request.user)

    @swagger_auto_schema(tags=['BusinessDirectory'])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception as response:
            return response
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

class PopularBusinessListingView(APIView):
    @swagger_auto_schema(tags=['BusinessDirectory'])
    def get(self, request, format=None):
        """
        Retrieve popular business listings
        popularity is based on the number of ratings
        """
        popular_businesses = BusinessListingRating.objects.values(
            "listing").annotate(avg_rating=Avg("value")
            ).order_by("-avg_rating")

        serializer = BusinessListingSerializer(popular_businesses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BusinessListingCategoryListView(APIView):
    @swagger_auto_schema(tags=['BusinessDirectory'])
    def get(self, request, format=None):
        """
        Retrieve all business listing categories from the database
        """
        categories = BusinessListingCategory.objects.all()
        serializer = BusinessListingCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PopularBusinessListingCategoryListView(APIView):
    @swagger_auto_schema(tags=['BusinessDirectory'])
    def get(self, request, format=None):
        """
        Retrieve popular business listing categories
        popularity is based on the number of associated businesses
        """
        popular_categories = BusinessListingCategory.objects.annotate(
            num_businesses=Count("listings")
        ).order_by("-num_businesses")

        serializer = BusinessListingCategorySerializer(popular_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BusinessLoanRequestView(generics.CreateAPIView):
    serializer_class = BusinessLoanRequestSerializer    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)

    @swagger_auto_schema(tags=['BusinessDirectory'])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
