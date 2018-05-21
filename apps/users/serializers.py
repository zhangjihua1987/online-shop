import datetime
import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

from MxShop.settings import REGEX_MOBILE
from .models import VerifyCode

USER = get_user_model()


class MobileSerializer(serializers.Serializer):
    """
    手机号验证
    """
    mobile = serializers.CharField(max_length=11)

    # 验证字段的逻辑，命名方式固定为validate_+字段名称
    def validate_mobile(self, mobile):
        """
        验证手机号码
        """

        # 验证手机是否已注册
        if USER.objects.filter(mobile=mobile):
            raise serializers.ValidationError('用户已存在')

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('请输入正确的手机号')

        # 控制验证频率
        one_minute_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile):
            raise serializers.ValidationError('请一分钟后重试')
        return mobile


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户注册验证
    """
    code = serializers.CharField(
        max_length=4,
        min_length=4,
        required=True,

        # 设置为只写字段，最后不会被序列化
        write_only=True,

        # drf的提示文本
        help_text='验证码',

        # 设置显示名字
        label='验证码',

        # 错误类型的返回信息设置
        error_messages={
            "blank": "请输入验证码",
            "max_length": "请输入正确的格式",
            "min_length": "请输入正确的格式"
        }
    )

    username = serializers.CharField(
        required=True,

        # 使用drf提供的validator，validator为list
        validators=[

            # 使用验证唯一性的方法
            UniqueValidator(

                # queryset为验证的对象
                queryset=USER.objects.all(),

                # 错误提示文本
                message='用户已经存在'
            )
        ],
        label='用户名'
    )

    password = serializers.CharField(
        required=True,

        # 设置为只写模式，避免传回被截获
        write_only=True,

        # 设置输入的模式为'password'
        style={
            'input_type': 'password'
        },
        label='密码'
    )

    # def create(self, validated_data):
    #     """
    #     重构create方法，利用signal也可以实现为密码加密
    #     """
    #
    #     # 使用super方法调用父类的create方法，创建一个数据表并实例化
    #     user = super(UserRegisterSerializer, self).create(validated_data=validated_data)
    #
    #     # 使用加密方式保存用户的密码至数据库
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    def validate_code(self, code):
        """
        验证code的逻辑，定义方式固定为validate_+字段名称
        """

        # # 用get方法需要捕获错误
        # try:
        #     verify_code = VerifyCode.objects.get(code=code, mobile=self.initial_data['username'])
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass

        # 用filter方法查询不到或者有多个查询结果都不会报错
        verify_code = VerifyCode.objects.filter(
            code=code,

            # 这里只能将code传递进来，所以mobile就只能用这种方式取到
            mobile=self.initial_data['username']

            # 这里要作排序，如果有多条数据需要取到最近的一条
        ).order_by('-add_time')

        # 判断验证码是否存在
        if verify_code:
            last_record = verify_code[0]

            # 取到5分钟之前的时间
            five_minutes_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=5, seconds=0)

            # 判断最近一条验证码添加时间小于5分钟之前的时间，判定为过期
            if last_record.add_time < five_minutes_ago:
                raise serializers.ValidationError('验证码过期')

        # 若验证码不存在说明验证码错误
        else:
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        """
        重构validate方法
        """

        # 将username赋值给mobile
        attrs['mobile'] = self.initial_data['username']

        # 删除只用于验证，不用于保存的字段code
        del attrs['code']
        return attrs

    class Meta:
        model = USER

        # 这里指定了3个字段，若前端只将电话号码作为username传递过来，需要将mobile字段设置为允许为空
        fields = ('username', 'code', 'mobile', 'password')


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    username = serializers.CharField(read_only=True)

    class Meta:
        model = USER
        fields = ('username', 'birthday', 'gender', 'email', 'mobile', 'name')

