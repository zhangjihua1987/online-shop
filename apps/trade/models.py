from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Goods


USER = get_user_model()
# Create your models here.


class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(USER, on_delete=models.CASCADE, verbose_name='用户')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    nums = models.IntegerField(default=0, verbose_name='商品数量')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'goods')

    def __str__(self):
        return '%s(%s)' % (self.user.name, self.nums)


class OrderInfo(models.Model):
    """
    订单
    """
    PAY_STATUS = (
        ('WAIT_BUYER_PAY', '交易创建'),
        ('TRADE_CLOSED', '超时关闭'),
        ('TRADE_SUCCESS', '支付成功'),
        ('TRADE_FINISHED', '交易结束'),
        ('unpaid', '待支付')
    )

    user = models.ForeignKey(USER, on_delete=models.CASCADE, verbose_name='用户')
    order_sn = models.CharField(max_length=100, verbose_name='订单编号', null=True, blank=True)
    trade_no = models.CharField(max_length=100, verbose_name='交易编号')
    pay_status = models.CharField(choices=PAY_STATUS, max_length=30, verbose_name='交易状态', default='unpaid')
    post_script = models.CharField(max_length=200, verbose_name='订单留言', default='')
    order_mount = models.FloatField(default=0.0, verbose_name='订单金额')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')

    # 收货信息
    address = models.CharField(max_length=300, verbose_name='收货地址')
    signer_name = models.CharField(max_length=50, verbose_name='签收人')
    signer_mobile = models.CharField(max_length=11, verbose_name='联系电话')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_sn


class OrderGoods(models.Model):
    """
    订单商品
    """
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name='所属订单', related_name='goods')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    goods_num = models.IntegerField(default=0, verbose_name='商品数量')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)


class OrderShoppingCart(models.Model):
    """
    购物车订单
    """
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name='所属订单', related_name='order_cart')
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, verbose_name='所属购物车')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '购物车订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order.order_sn


