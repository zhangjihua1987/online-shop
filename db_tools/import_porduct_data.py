import os

import django

from db_tools.data.product_data import row_data

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MxShop.settings')
django.setup()


class ImportProductData(object):
    """
    导入商品信息
    """
    def import_product_data(self, datas):
        from goods.models import Goods
        from goods.models import GoodsCategory
        from goods.models import GoodsImage
        for data in datas:
            good = Goods()
            good.name = data['name']

            # 商品类别为外键
            # 通过名称筛选出类别再赋值
            category = data['categorys'][-1]
            good_category = GoodsCategory.objects.filter(name=category)
            if category:
                good.category = good_category[0]

            good.market_price = float(data['market_price'].replace('￥', '').replace('元', ''))
            good.shop_price = float(data['sale_price'].replace('￥', '').replace('元', ''))
            good.goods_brief = data['desc'] if data['desc'] is not None else ''
            good.goods_front_image = data['images'][0] if data['images'] is not None else ''
            good.goods_desc = data['goods_desc'] if data['goods_desc'] is not None else ''
            good.save()

            if data['images'] is not None:
                for image in data['images']:
                    good_image = GoodsImage()
                    good_image.goods = good
                    good_image.image = image
                    good_image.save()


import_data = ImportProductData()
import_data.import_product_data(row_data)

