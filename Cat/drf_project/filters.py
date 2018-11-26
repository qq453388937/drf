# -*- coding:utf-8 -*-

from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Goods
import django_filters


class GoodsFilter(filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr="gt")
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    # 模糊查询
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    top_category = django_filters.NumberFilter(method='top_category_filter', label='top_category')

    def top_category_filter(self, queryset, name, value):
        """ 创建自己的过滤器 """
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['min_price', 'max_price', 'name']
