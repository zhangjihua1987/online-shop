from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utils.permissions import IsOwnerOrReadOnly
from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserFavDetailSerializer, UserLeavingMessageSerializer, UserAddressSerializer

# Create your views here.


class UserFavViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    list:
        获取用户收藏详情

    retrieve:
        判断用户收藏是否存在

    create:
        创建用户收藏
    """
    # 权限验证类型
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    # 登录验证了类型
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 设置retrieve的搜索字段，因为前端传递进来的是商品的ID
    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer
        else:
            return UserFavSerializer

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)


class UserLeavingMessageViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    list:
        获取所有留言

    destroy:
        删除留言

    create:
        创建留言
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = UserLeavingMessageSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class UserAddressViewSet(viewsets.ModelViewSet):
    """
    list:
        获取全部地址

    retrieve:
        获取地址详情

    create:
        创建地址

    destroy:
        删除地址
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
