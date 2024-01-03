from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    def __init__(self, page_size=10, page_size_query_param='page_size', max_page_size=1000):
        self.page_size = page_size
        self.page_size_query_param = page_size_query_param
        self.max_page_size = max_page_size

