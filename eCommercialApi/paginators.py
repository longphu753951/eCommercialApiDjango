from rest_framework import pagination


class ProductPaginator(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
