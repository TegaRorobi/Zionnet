from django.urls import path
from .views import *

app_name = 'JobPosting'
urlpatterns = [
    path('jobs/search/', JobSearchView.as_view(), name='job-search'),
    path('jobs/sort/', JobSortView.as_view(), name='job-sort'),
    path('jobs/categories/', JobCategoryView.as_view(), name='job-categories'),
    path('jobs/categories/<int:category_id>/jobs/', GetJobsByCategory.as_view(), name='jobs-in-category'),
]
