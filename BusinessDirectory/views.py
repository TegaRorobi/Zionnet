from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import BusinessListingRequest, BusinessListing
from .serializers import BusinessListingRequestSerializer, BusinessListingSerializer

class BusinessListingRequestCreateView(generics.CreateAPIView):
    queryset = BusinessListingRequest.objects.all()
    serializer_class = BusinessListingRequestSerializer

    def perform_create(self, serializer):
        serializer.save(vendor_id=self.request.user)

class BusinessListingVendorRequestCreateView(generics.CreateAPIView):
    queryset = BusinessListing.objects.all()
    serializer_class = BusinessListingSerializer

    def perform_create(self, serializer):
        return Response("Vendor request and listing created successfully.", status=status.HTTP_201_CREATED)
