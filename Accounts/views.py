from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics,permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import LogoutSerializer, RegistrationSerializer
from drf_yasg.utils import swagger_auto_schema

class RegistrationAPIView(generics.GenericAPIView):
    serializer_class=RegistrationSerializer
    permission_classes = []
    @swagger_auto_schema(tags=['Accounts'])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    @swagger_auto_schema(tags=['Accounts'])
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

class LoginRefreshView(TokenRefreshView):
    @swagger_auto_schema(tags=['Accounts'])
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = []

    @swagger_auto_schema(tags=['Accounts'])
    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message':'You have logged out successfully'},status=status.HTTP_204_NO_CONTENT)