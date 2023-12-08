from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import *
from .serializers import *

class JobSearchView(APIView):
    "API View to search for jobs using the job title, the required skills and also category"
    @swagger_auto_schema(tags=['JobPosting - search'])
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
    @swagger_auto_schema(tags=['JobPosting - sort'])
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
    
    @swagger_auto_schema(tags=['JobPosting - all categories'])
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
    @swagger_auto_schema(tags=['JobPosting - get job by category'])
    def get(self, request, category_id):
        try:
            category = JobCategory.objects.get(pk=category_id)
        except JobCategory.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        jobs = JobOpening.objects.filter(category=category)
        serialized_jobs = JobOpeningSerializer(jobs, many=True)
        return Response({'data': serialized_jobs.data},
        status=status.HTTP_200_OK)
        