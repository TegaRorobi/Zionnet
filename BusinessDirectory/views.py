from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import BusinessListing, BusinessListingRating
from .serializers import BusinessListingSerializer, BusinessListingRatingSerializer
from django.http import Http404
from rest_framework import status
from django.db.models import Avg

#endpoint to Retrieve top-rated listings based on average rating
class TopRatedListingsView(generics.ListAPIView):
    permission_classes = []
    serializer_class = BusinessListingSerializer
    
    def get_queryset(self):
        try:
            top_rated_listings = BusinessListing.objects.annotate(avg_rating=Avg('ratings__value')).order_by('-avg_rating')[:5]
            return top_rated_listings
        except Exception as e:
            error_message = str(e)
            response = {
                'status_message': 'error',
                'message': 'An error occurred: ' + error_message,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
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
    # permission_classes = [IsAuthenticated]
    permission_classes = []

    def get_queryset(self):
        try:
            return BusinessListing.objects.filter(vendor_id=self.request.user)
        except Exception as e:
            raise Exception(str(e))
        # except Exception as e:
        #     error_message = str(e)
        #     response = {
        #         'status_message': 'error',
        #         'message': 'An error occurred: ' + error_message,
        #     }
        #     return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # def list(self, request, *args, **kwargs):
    #     try:
    #         queryset = self.get_queryset()
    #         serializer = self.get_serializer(queryset, many=True)
    #         return Response(serializer.data)
    #     except Exception as e:
    #         error_message = str(e)
    #         response = {
    #             'status_message': 'error',
    #             'message': 'An error occurred: ' + error_message,
    #         }
    #         return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

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