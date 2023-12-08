
from django.urls import re_path, path
from .views import *

app_name = 'JobPosting'

urlpatterns = [
    re_path(
        '^freelancer/create/?$', 
        FreelancerProfileView.as_view({'post': 'create_freelancer_profile'}),
        name='freelancer-profile-create'
    ),
    re_path(
        '^me/job-application/create/?$',
        JobApplicationView.as_view({'post': 'create_job_application'}),
        name='job-application-create'
    ),
    re_path(
        '^me/job-applications/?$',
        JobApplicationView.as_view({'get': 'get_job_applications'}),
        name='job-applications-list'
    ),
    path('jobs/search/', JobSearchView.as_view(), name='job-search'),
    path('jobs/sort/', JobSortView.as_view(), name='job-sort'),
    path('jobs/categories/', JobCategoryView.as_view(), name='job-categories'),
    path('jobs/categories/<int:category_id>/jobs/', GetJobsByCategory.as_view(), name='jobs-in-category'),
    
    path('jobs/featured/', FeaturedJobsAPIView.as_view(), name='featured-jobs'),
    path('jobs/best-match/', BestMatchJobsAPIView.as_view(), name='best-match-jobs'),
    path('jobs/most-recent/', MostRecentJobsAPIView.as_view(), name='most-recent-jobs'),
]
