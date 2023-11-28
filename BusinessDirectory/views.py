from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import BusinessListing
from .serializers import BusinessListingSerializer
from django.http import Http404
from rest_framework import status

@api_view(['GET'])
@permission_classes([AllowAny])
def top_rated_listings(request):
    try:
        top_rated_listings = BusinessListing.objects.order_by('-rating')[:5]
        serializer = BusinessListingSerializer(top_rated_listings, many=True)
        return Response(serializer.data)
    except Exception as e:
        error_message = str(e)
        response = {
            'status_message': 'error',
            'message': 'An error occurred: ' + error_message,
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def user_listings(request):
    try:
        user_listings = BusinessListing.objects.filter(vendor_id=request.user.id)
        serializer = BusinessListingSerializer(user_listings, many=True)
        return Response(serializer.data)
    except Exception as e:
        error_massage = str(e)
        response = {
            'status_massage': 'error',
            'massage' : 'An error has occurred: ' + error_massage,
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
class Business_listing(generics.RetrieveAPIView):
    def get_object(self, pk):
        try:
            return BusinessListing.objects.get(pk=pk)
        except BusinessListing.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, *args, **kwarge):
        instance = self.get_object(pk)
        serializer = BusinessListingSerializer(instance)
        return Response(serializer.data)
    
    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return Response({"error": "Business not found"}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)
