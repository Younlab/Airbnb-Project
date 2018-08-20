from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    """
    Pagination
    """
    page_size = 18
    page_query_param = 'page'