from django.db.models import Q
from rest_framework import serializers

from .models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand, IndexAD


class GoodsCategorySerializer3(serializers.ModelSerializer):
    """
    商品三级类目ModelSerializer
    """
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsCategorySerializer2(serializers.ModelSerializer):
    """
    商品二级类目ModelSerializer
    """
    sub_cat = GoodsCategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsCategorySerializer(serializers.ModelSerializer):
    """
    商品一级类目ModelSerializer
    """
    sub_cat = GoodsCategorySerializer2(many=True)

    # 指定对应的model及字段
    # 可以用fields = ('name', 'category', ....)的形式来指定想要的字段
    # 也可以用'__all__'可以选定全部字段
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    """
    商品图片
    """
    class Meta:
        model = GoodsImage
        fields = ('image', )


class GoodsSerializer(serializers.ModelSerializer):
    """
    商品ModelSerializer
    """
    # 可以用这种方式指定外键，将外键的所有信息包括到GoodsSerializer中
    category = GoodsCategorySerializer()

    # 这里可以用外键字段中定义的relate_name来从外键反取
    # 如果外键有多个值，需要设置many=True参数
    image = ImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    """
    首页轮播图序列化类
    """
    class Meta:
        model = Banner
        fields = '__all__'


class GoodsCategoryBrandSerializer(serializers.ModelSerializer):
    """
    商家广告序列化类
    """
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'


class ADGoodsSerializer(serializers.ModelSerializer):
    """
    广告商品序列化类
    """

    class Meta:
        model = Goods
        fields = ('id', 'goods_front_image')


class IndexCategorySerializer(serializers.ModelSerializer):
    """
    首页广告序列化类
    """
    brands = GoodsCategoryBrandSerializer(many=True)
    sub_cat = GoodsCategorySerializer2(many=True)
    goods = serializers.SerializerMethodField()
    ad_goods = serializers.SerializerMethodField()

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) |
                                         Q(category__parent_category_id=obj.id) |
                                         Q(category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    def get_ad_goods(self, obj):
        ad_goods = IndexAD.objects.filter(category_id=obj.id)[0].goods
        if ad_goods:
            ad_goods = ADGoodsSerializer(ad_goods, context={'request': self.context['request']}).data
        return ad_goods

    class Meta:
        model = GoodsCategory
        fields = '__all__'
