from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BusinessListing
from .pagination import ListingPagination
from .serializers import BusinessListingSerializer
from .permissions import IsVendorVerified

class BusinessListingListCreateView(generics.ListCreateAPIView):
    queryset = BusinessListing.objects.all()
    serializer_class = BusinessListingSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'city', 'province', 'country',
    'phone_number']
    ordering_fields = ['name', 'created_at']  
    ordering = ['-created_at']  
    pagination_class = ListingPagination
    permission_classes = [IsVendorVerified]
    
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        images = BusinessListingImage.objects.filter(listing=instance)
        image_serializer = BusinessListingImageSerializer(images, many=True)
        response_data = serializer.data
        response_data['images'] = image_serializer.data

        return Response(response_data)
        
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        images_data = self.request.FILES.getlist('images', [])
        files_data = self.request.FILES.getlist('files', [])

        # Save associated images
        for image_data in images_data:
            image_serializer = BusinessListingImageSerializer(data={'image': image_data, 'listing': business_listing.id})
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save()
        
        for file_data in files_data:
            file_serializer = BusinessListingFileSerializer(data={'file': file_data, 'listing': business_listing.id})
            file_serializer.is_valid(raise_exception=True)
            file_serializer.save()
    
        serializer.is_valid(raise_exception=True)
        business_listing = serializer.save(vendor_id=self.request.user)
       
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Response as response:
            return response
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)