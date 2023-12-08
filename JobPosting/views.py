
from rest_framework import (
    decorators, viewsets, mixins, permissions, status
)
from rest_framework.settings import api_settings
from rest_framework.response import Response
from .permissions import HasFreelancerProfile
from .serializers import *
from .models import *



class FreelancerProfileView(viewsets.GenericViewSet, mixins.CreateModelMixin):

    serializer_class = FreelancerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.action(detail=True)
    def create_freelancer_profile(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobApplicationView(viewsets.GenericViewSet, mixins.CreateModelMixin):

    serializer_class = JobApplicationSerializer
    permission_classes = [HasFreelancerProfile]

    @decorators.action(detail=True)
    def create_job_application(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(applicant=request.user.freelancer_profile)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
