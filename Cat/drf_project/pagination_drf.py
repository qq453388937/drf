# -*- coding:utf-8 -*-
from rest_framework.pagination import PageNumberPagination


class Goods_pagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "qq"   # 定制page_size
    page_query_param = "pp"  # 定制pageIndex参数
    max_page_size = 10
