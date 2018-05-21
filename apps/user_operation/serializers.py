import re
from MxShop.settings import REGEX_MOBILE
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from goods.serializers import GoodsSerializer

from .models import UserFav, UserLeavingMessage, UserAddress
from users.serializers import UserDetailSerializer


class UserFavDetailSerializer(serializers.ModelSerializer):
    """
    用户收藏详情序列化类
    """
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ('goods', 'id')


class UserFavSerializer(serializers.ModelSerializer):
    """
    用户收藏序列化类
    """
    # 将user字段隐藏，并设置默认值为当前的user
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        fields = ('user', 'goods', 'id')

        # 这里使用drf的联合唯一字段验证，避免重复收藏，如果在model中设置过unique_together字段，这里就只是更改了错误提示
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message='收藏信息已存在'
            )
        ]


class UserLeavingMessageSerializer(serializers.ModelSerializer):
    """
    用户留言序列化类
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserLeavingMessage
        fields = ('user', 'msg_type', 'subject', 'message', 'file', 'add_time', 'id')


class UserAddressSerializer(serializers.ModelSerializer):
    """
    用户地址序列化类
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    province = serializers.CharField(required=True,
                                     error_messages={
                                         'required': '不能为空',
                                         'min_length': '请输入正确的省份'
                                     })
    city = serializers.CharField(required=True,
                                 error_messages={
                                     'required': '不能为空',
                                     'min_length': '请输入正确的城市'
                                 })
    area = serializers.CharField(required=True,
                                     error_messages={
                                         'required': '不能为空',
                                         'min_length': '请输入正确的区域'
                                     })
    address = serializers.CharField(required=True,
                                    error_messages={
                                        'required': '不能为空',
                                    })
    signer_name = serializers.CharField(required=True,
                                        error_messages={
                                            'required': '不能为空',
                                        })
    signer_mobile = serializers.CharField(required=True,
                                          error_messages={
                                              'required': '不能为空'
                                          })

    def validate_signer_mobile(self, signer_mobile):
        if not re.match(REGEX_MOBILE, signer_mobile):
            raise serializers.ValidationError('请输入正确的手机号')
        return signer_mobile

    class Meta:
        model = UserAddress
        fields = ('id', 'user', 'province', 'city', 'area', 'address', 'signer_name', 'signer_mobile', 'add_time')
