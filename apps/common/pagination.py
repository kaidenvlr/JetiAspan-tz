from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size = 1
    page_size_query_param = 'per_page'
    max_page_size = 100
