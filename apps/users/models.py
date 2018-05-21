from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    """
    用户信息
    """
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='姓名')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name='手机号')
    gender = models.CharField(
        choices=(('male', '男'), ('female', '女')),
        default='male', verbose_name='性别', max_length=7)
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='邮箱地址')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code




