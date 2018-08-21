from rest_framework.pagination import PageNumberPagination

__all__ = (
    'Pagination',
)


class Pagination(PageNumberPagination):
    """
    Pagination
    """
    page_size = 1000
    page_query_param = 'page'
