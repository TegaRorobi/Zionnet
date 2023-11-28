from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10
class ListingPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'
    
    def get_total_pages(self):
             # Calculate the total pages based on count and page size
              count = self.page.paginator.count
              page_size = self.page.paginator.per_page
              return (count + page_size- 1) // page_size
     
    def get_paginated_response(self, data,):
        return Response({
            'total': self.page.paginator.count,
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)),
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'total_pages': self.get_total_pages(),
            'current_page': self.page.number,
            'results': data
        })
        
