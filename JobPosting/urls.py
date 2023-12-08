
from django.urls import re_path
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
    )
]