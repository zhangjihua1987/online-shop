from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Goods


class GoodsFilters(filters.FilterSet):
    """
    商品过滤
    """
    # 定义搜索的字段，类似于ModelForm以及ModelSerializer
    # 参数name为字段名称，lookup_expr为操作类型
    pricemin = filters.NumberFilter(name='shop_price', lookup_expr='gte')
    pricemax = filters.NumberFilter(name='shop_price', lookup_expr='lte')
    top_category = filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(
            Q(category_id=value) |
            Q(category__parent_category_id=value) |
            Q(category__parent_category__parent_category_id=value)
        )

    class Meta:
        # 配置指定的model，和fields
        model = Goods
        fields = ('pricemin', 'pricemax', 'is_hot', 'is_new')

