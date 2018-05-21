from datetime import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer, OrderInfoSerializer, OrderDetailSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods
from utils.permissions import IsOwnerOrReadOnly
from utils.alipay import AliPay
from MxShop.settings import PRIVATE_KEY_PATH, ALIPAY_KEY_PATH
# Create your views here.


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    list:
        获取当前用户所有购物车信息
    create:
        创建购物车
    retrieve:
        获取购物车详情
    destroy:
        删除购物车
    """
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    lookup_field = 'goods_id'

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ShoppingCartDetailSerializer
        else:
            return ShoppingCartSerializer

    def perform_create(self, serializer):
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    def perform_update(self, serializer):
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        save_record = serializer.save()
        goods = serializer.instance.goods
        delta_nums = existed_record.nums - save_record.nums
        goods.goods_num += delta_nums
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    订单管理

    create:
        创建订单

    destroy:
        删除订单

    list:
        获取所有订单

    retrieve:
        获取订单详情
    """
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        else:
            return OrderInfoSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()
        shopping_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shopping_cart in shopping_carts:
            OrderGoods.objects.create(order=order, goods=shopping_cart.goods, goods_num=shopping_cart.nums)
            shopping_cart.delete()
        return order


class AlipayView(APIView):
    """
    处理支付宝返回信息
    """
    def get(self, request):
        """
        处理return_url
        """
        process_dict = dict()
        for key, value in request.GET.items():
            process_dict[key] = value
        ali_sign = process_dict.pop('sign')

        alipay = AliPay(
            appid="2016091500518447",
            app_notify_url="http://47.106.173.70:8000/alipay/return/",
            app_private_key_path=PRIVATE_KEY_PATH,
            alipay_public_key_path=ALIPAY_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.106.173.70:8000/alipay/return/"
        )

        res_verify = alipay.verify(process_dict, ali_sign)
        if res_verify:
            order_infos = OrderInfo.objects.filter(order_sn=process_dict['out_trade_no'])
            for order_info in order_infos:

                # OrderGoods中设置了外键指向OrderInfo，
                # related_name设置为goods可以通过OrderInfo.goods.all()取出所有的OrderGoods
                all_order_goods = order_info.goods.all()
                for order_goods in all_order_goods:
                    goods = order_goods.goods
                    goods.sold_num += order_goods.goods_num
                    goods.save()

            from django.shortcuts import redirect
            response = redirect('index')
            response.set_cookie('nextPath', 'pay', max_age=3)
            return response
        else:
            from django.shortcuts import redirect
            response = redirect('index')
            return response

    def post(self, request):
        """
        处理notify_url
        """
        process_dict = dict()
        for key, value in request.POST.items():
            process_dict[key] = value
        ali_sign = process_dict.pop('sign')

        alipay = AliPay(
            appid="2016091500518447",
            app_notify_url="http://47.106.173.70:8000/alipay/return/",
            app_private_key_path=PRIVATE_KEY_PATH,
            alipay_public_key_path=ALIPAY_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.106.173.70:8000/alipay/return/"
        )

        res_verify = alipay.verify(process_dict, ali_sign)
        if res_verify:
            order_infos = OrderInfo.objects.filter(order_sn=process_dict['out_trade_no'])
            for order_info in order_infos:
                order_info.trade_no = process_dict.get('trade_no', None)
                order_info.pay_status = process_dict.get('trade_status', None)
                order_info.pay_time = datetime.now()
                order_info.save()

            return Response("success")


