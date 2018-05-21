# Create your views here.

from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_extensions.cache.mixins import CacheResponseMixin       # 导入关于drf_extensions的缓存配置，加入到viewset中就可以使用了
from rest_framework.authentication import TokenAuthentication

from .models import Goods, GoodsCategory, Banner
from .serializers import GoodsSerializer, GoodsCategorySerializer, BannerSerializer, IndexCategorySerializer
from .filters import GoodsFilters


class GoodsPagenation(PageNumberPagination):
    """
    商品分页
    """
    # 设置每页数量
    page_size = 12

    # 设置每页数量的变量名
    # 例如可以在域名中加上page_size=50实现每页取出50个数据
    page_size_query_param = 'page_size'


class GoodsListViewSet(CacheResponseMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    商品列表页（分页、过滤、搜索及排序）
    """

    # 重构queryset以及serializer_class
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    # 指定分页的类
    pagination_class = GoodsPagenation

    # 配置filter_backends
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    # 配置过滤类
    filter_class = GoodsFilters

    # 配置搜索字段
    search_fields = ('name', 'goods_brief', 'goods_desc')

    # 配置排序的字段
    ordering_fields = ('sold_num', 'shop_price')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GoodsCategoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    list:
        商品类目列表
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = GoodsCategorySerializer


class BannerViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    list:
        获取全部轮播图
    """
    queryset = Banner.objects.all().order_by('index')[:3]
    serializer_class = BannerSerializer


class IndexCategoryViewSet(ListModelMixin, GenericViewSet):
    """
    list:
        获取首页商品类别
    """
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=['生鲜食品', '酒水饮料'])
    serializer_class = IndexCategorySerializer
