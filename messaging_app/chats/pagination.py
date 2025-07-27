from rest_framework import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
  page_size = 20
  max_page_size = 20
  