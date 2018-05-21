from random import Random
import time
from rest_framework import serializers

from goods.models import Goods
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer
from utils.alipay import AliPay
from MxShop.settings import PRIVATE_KEY_PATH, ALIPAY_KEY_PATH


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    """
    购物车详情序列化类
    """
    goods = GoodsSerializer()

    class Meta:
        model = ShoppingCart
        fields = '__all__'


class ShoppingCartSerializer(serializers.Serializer):
    """
    购物车序列化类
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(), required=True, )

    nums = serializers.IntegerField(required=True, min_value=1,
                                    error_messages={
                                      'required': '不能为空',
                                      'min_value': '至少选择一个商品'
                                    })

    def create(self, validated_data):
        shopping_cart = ShoppingCart.objects.filter(user=validated_data['user'], goods=validated_data['goods'])
        if shopping_cart:
            shopping_cart = shopping_cart[0]
            shopping_cart.nums += validated_data['nums']
            shopping_cart.save()
        else:
            shopping_cart = ShoppingCart.objects.create(**validated_data)
        return shopping_cart

    def update(self, instance, validated_data):
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class OrderInfoSerializer(serializers.ModelSerializer):
    """
    订单创建序列化类
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        """
        生成支付宝url
        """
        alipay = AliPay(
            appid="2016091500518447",
            app_notify_url="http://47.106.173.70:8000/alipay/return/",
            app_private_key_path=PRIVATE_KEY_PATH,
            alipay_public_key_path=ALIPAY_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.106.173.70:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )

        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url



    def generate_order_sn(self):
        """
        生成订单号，时间+用户id+2位随机数
        """
        random_str = Random()
        order_sn = '%s%s%s' % (time.strftime('%Y%m%d%H%M%S'), self.context['request'].user.id,
                               random_str.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderGoodsSerializer(serializers.ModelSerializer):
    """
    订单商品序列化类
    """
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    订单详情序列化类
    """
    goods = OrderGoodsSerializer(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        """
        生成支付宝url
        """
        alipay = AliPay(
            appid="2016091500518447",
            app_notify_url="http://47.106.173.70:8000/alipay/return/",
            app_private_key_path=PRIVATE_KEY_PATH,
            alipay_public_key_path=ALIPAY_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.106.173.70:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )

        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    class Meta:
        model = OrderInfo
        fields = '__all__'
