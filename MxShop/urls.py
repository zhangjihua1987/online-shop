"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
import xadmin
from django.urls import path, re_path, include
from django.views.static import serve
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from .settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, GoodsCategoryViewSet, BannerViewSet, IndexCategoryViewSet
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet, UserLeavingMessageViewSet, UserAddressViewSet
from trade.views import ShoppingCartViewSet, OrderViewSet, AlipayView

router = DefaultRouter()
router.register('goods', GoodsListViewSet, base_name='goods_list')
router.register('categorys', GoodsCategoryViewSet, base_name='category_list')
router.register('codes', SmsCodeViewSet, base_name='codes')
router.register('users', UserViewSet, base_name='register')
router.register('userfavs', UserFavViewSet, base_name='userfavs')
router.register('messages', UserLeavingMessageViewSet, base_name='messages')
router.register('address', UserAddressViewSet, base_name='address')
router.register('shopcarts', ShoppingCartViewSet, base_name='shopcarts')
router.register('orders', OrderViewSet, base_name='orders')
router.register('banners', BannerViewSet, base_name='banners')
router.register('indexgoods', IndexCategoryViewSet, base_name='indexgoods')


urlpatterns = [
    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),

    path('xadmin/', xadmin.site.urls),

    # 图片访问url
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # browsable API
    path('api-auth/', include('rest_framework.urls')),

    # drf文档功能
    path('docs/', include_docs_urls(title='慕学生鲜')),

    # router的url配置
    path('', include(router.urls)),

    # token auth的api配置
    path('api-token-auth/', views.obtain_auth_token),

    # JWT auth的api配置
    re_path('^login/$', obtain_jwt_token),

    # 处理支付宝返回信息的url
    path('alipay/return/', AlipayView.as_view(), name='alipay'),

    # 第三方登录验证url
    path('', include('social_django.urls', namespace='social'))

]
