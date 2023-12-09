
from rest_framework import (
    decorators, viewsets, mixins, permissions, status, generics
)
from drf_yasg.utils import swagger_auto_schema
from helpers.pagination import PaginatorGenerator
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import HasFreelancerProfile
from .serializers import *
from .models import *


class FreelancerProfileView(viewsets.GenericViewSet, mixins.CreateModelMixin):

    serializer_class = FreelancerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.action(detail=True)
    @swagger_auto_schema(tags=['JobPosting'])
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
    pagination_class = PaginatorGenerator()(_page_size=10)

    def get_queryset(self):
        return JobApplication.objects.filter(
            applicant = self.request.user.freelancer_profile
        ).order_by('-updated_at')

    @decorators.action(detail=True)
    @swagger_auto_schema(tags=['JobPosting'])
    def create_job_application(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(applicant=request.user.freelancer_profile)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(detail=False)
    @swagger_auto_schema(tags=['JobPosting'])
    def get_job_applications(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JobSearchView(APIView):

    "API View to search for jobs using the job title, the required skills and also category"

    @swagger_auto_schema(tags=['JobPosting'])
    def post(self, request):
        try:
            title = request.data.get('title', None)
            category = request.data.get('category', None)
            skills = request.data.get('skills', [])

            queryset = JobOpening.objects.all()
            if title:
                queryset = queryset.filter(title__icontains=title)
            if category:
                queryset = queryset.filter(category__name=category)
            if skills:
                queryset = queryset.filter(required_skills__name__in=skills)

            serialized_jobs = JobOpeningSerializer(queryset, many=True)
            return Response({'data': serialized_jobs.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JobSortView(APIView):

    "API View to sort jobs using the meta fields and return a response ordered by the latest job"

    @swagger_auto_schema(tags=['JobPosting'])
    def post(self, request):
        try:
            sort_by = request.data.get('sort_by', None)
            reverse_order = request.data.get('reverse', False)
            
            if not sort_by:
                return Response({'error': 'Missing "sort_by" parameter'}, status=status.HTTP_400_BAD_REQUEST)

            valid_fields = [field.name for field in JobOpening._meta.get_fields()]

            if sort_by not in valid_fields:
                return Response({'error': f'Invalid "sort_by" field. Valid values: {", ".join(valid_fields)}'},
                                status=status.HTTP_400_BAD_REQUEST)

            jobs = JobOpening.objects.order_by(sort_by)
            
            # reverse the order of sorted jobs data
            if reverse_order == 'true':
                jobs = jobs.reverse()

            serialized_jobs = JobOpeningSerializer(jobs, many=True)
            return Response({'data': serialized_jobs.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class JobCategoryView(APIView):

    "API View to get all jobs categories "
    
    @swagger_auto_schema(tags=['JobPosting'])
    def get(self, request):
        try:
            categories = JobCategory.objects.all()
            serialized_categories = JobCategorySerializer(categories, many=True)
            return Response({'data': serialized_categories.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetJobsByCategory(APIView):

    "API View to get a job belonging to a category"

    @swagger_auto_schema(tags=['JobPosting'])
    def get(self, request, category_id):
        try:
            category = JobCategory.objects.get(pk=category_id)
        except JobCategory.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        jobs = JobOpening.objects.filter(category=category)
        serialized_jobs = JobOpeningSerializer(jobs, many=True)
        return Response({'data': serialized_jobs.data},
        status=status.HTTP_200_OK)
        

class CompanyListView(APIView):
    """ A view for retrieving all companies """
    @swagger_auto_schema(tags=['JobPosting'])
    def get(self, request, *args, **kwargs):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TopCompaniesView(APIView):
    """A view to retrieve companies with the highest number of employees"""

    @swagger_auto_schema(tags=['JobPosting'])
    def get(self, request, *args, **kwargs):
        top_companies = Company.objects.order_by('-employee_number_range')
        serializer = CompanySerializer(top_companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PostJobView(generics.CreateAPIView):
    """ This endpoint allows users to create a new job opening."""
    queryset = JobOpening.objects.all()
    serializer_class = JobOpeningSerializer

    @swagger_auto_schema(tags=['JobPosting'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        # Add the poster (user) information to the request data
        request.data['poster'] = request.user.id

        response = super().create(request, *args, **kwargs)
        return response
    
class CompanyJobsView(APIView):
    """A view for retrieving jobs posted in a company """

    @swagger_auto_schema(tags=['JobPosting'])
    def get(self, request, *args, **kwargs):
        company_id = kwargs.get('company_id')
        if company_id is not None:
            jobs = JobOpening.objects.filter(company__id=company_id)
            serializer = JobOpeningSerializer(jobs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Company ID is required'}, status=status.HTTP_400_BAD_REQUEST)