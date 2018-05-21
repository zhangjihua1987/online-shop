import random
import string

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from .serializers import MobileSerializer, UserRegisterSerializer, UserDetailSerializer
from MxShop.settings import YP_APIKEY
from utils.yunpian import YunPian
from .models import VerifyCode

# Create your views here.
USER = get_user_model()


class CustomAuthBackend(ModelBackend):
    """
    自定义登录验证方式
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = USER.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, GenericViewSet):
    """
    短信验证码
    """
    serializer_class = MobileSerializer

    def generate_code(self, k):
        """
        生成随机数
        小于10时为纯数字
        """
        if k < 10:
            seed = string.digits
        else:
            seed = string.digits + string.ascii_letters
        code = ''.join(random.choices(population=seed, k=k))
        return code

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        yun_pian = YunPian(YP_APIKEY)
        code = self.generate_code(4)
        re_msg = yun_pian.send_sms(code=code, mobile=mobile)
        if re_msg['code'] != 0:
            return Response({
                "mobile": re_msg['detail']
            }, status.HTTP_400_BAD_REQUEST)
        else:
            VerifyCode.objects.create(code=code, mobile=mobile)
            return Response({
                "mobile": mobile
            }, status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """
    用户
    """
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)

    def get_permissions(self):
        """
        重载权限验证方法
        """
        if self.action == 'retrieve':

            # 这里返回的要直接调用方法
            return [IsAuthenticated()]
        elif self.action == 'create':
            return []
        else:
            return []

    def get_serializer_class(self):
        """
        重载获取serializer的方法
        """
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegisterSerializer
        else:
            return UserDetailSerializer

    def create(self, request, *args, **kwargs):
        """
        重构create方法，将前端需要的token、name等定制的信息返回
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 将perform_create重构后，这里可以用user接收，用于生成payload
        user = self.perform_create(serializer)

        # 生成jwt的方法
        # 从rest_framework_jwt导入jwt_payload_handler，jwt_encode_handler
        payload = jwt_payload_handler(user)

        # 用payload生成token
        serializer.data['token'] = jwt_encode_handler(payload)

        # 获取前端需要的字段，以后可以用这种方式完成定制化的返回。
        serializer.data['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """
        重构perform_create
        """
        # 加上return值用于接收保存的对象
        return serializer.save()

    def get_object(self):
        """
        重构获取对象的方法
        """
        return self.request.user
