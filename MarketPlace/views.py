
from rest_framework import generics, status, permissions
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

