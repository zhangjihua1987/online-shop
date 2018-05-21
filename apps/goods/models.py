from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

# Create your models here.


class GoodsCategory(models.Model):
    """
    商品类别
    """
    CATEGORY_TYPE = (
        (1, '一级类目'),
        (2, '二级类目'),
        (3, '三级类目')
        )
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='类别名称', help_text='类别名称')
    code = models.CharField(max_length=30, null=True, blank=True, verbose_name='类别编号', help_text='类别编号')
    desc = models.TextField(default='', verbose_name='类别描述', help_text='类别描述')
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name='类目级别', help_text='类目级别')
    parent_category = models.ForeignKey(
        'self', blank=True, null=True, verbose_name='父类别', related_name='sub_cat',
        on_delete=models.CASCADE
    )
    is_tab = models.BooleanField(default=False, verbose_name='是否导航', help_text='是否导航')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    品牌名
    """
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name='商品类别', null=True, blank=True,
                                 related_name='brands')
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='品牌名', help_text='品牌名')
    desc = models.TextField(blank=True, null=True, verbose_name='品牌描述', help_text='品牌描述')
    image = models.ImageField(max_length=200, upload_to='brands/', verbose_name='品牌logo')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '品牌名'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品
    """
    name = models.CharField(max_length=300, verbose_name='商品名')
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name='商品类别')
    good_sn = models.CharField(max_length=50, null=True, blank=True, verbose_name='商品编号')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    sold_num = models.IntegerField(default=0, verbose_name='销售数')
    fav_num = models.IntegerField(default=0, verbose_name='收藏数')
    goods_num = models.IntegerField(default=0, verbose_name='库存')
    market_price = models.IntegerField(default=0, verbose_name='市场价')
    shop_price = models.IntegerField(default=0, verbose_name='销售价')
    goods_brief = models.TextField(verbose_name='商品简短描述', default='')
    is_ship_free = models.BooleanField(default=False, verbose_name='是否免运费')
    goods_front_image = models.ImageField(upload_to='goods/images/', max_length=200, verbose_name='商品封面图')
    is_new = models.BooleanField(default=False, verbose_name='是否新品')
    is_hot = models.BooleanField(default=False, verbose_name='是否热销')
    goods_desc = UEditorField(
        verbose_name='内容',
        imagePath='goods/images/',
        width=1000,
        height=300,
        filePath='goods/files/',
        default=''
        )

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    """
    商品轮播图
    """
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品名称', related_name='image')
    image = models.ImageField(upload_to='goods/image/', verbose_name='详情轮播图片', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '商品轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    """
    轮播的商品
    """
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品名称')
    image = models.ImageField(upload_to='goods/image/', verbose_name='首页轮播图', max_length=100)
    index = models.IntegerField(default=100, verbose_name='轮播顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '首页轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class IndexAD(models.Model):
    """
    首页广告商品
    """
    goods = models.ForeignKey(Goods, related_name='goods', verbose_name='广告商品', on_delete=models.CASCADE)
    category = models.ForeignKey(GoodsCategory, related_name='category', verbose_name='广告类别',
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = '首页广告商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s/%s' % (self.category.name, self.goods.name)