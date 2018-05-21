import os
# import sys

import django

from db_tools.data.category_data import row_data


# pwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(pwd)

# 设置settings文件与项目settings文件一致
# 这里的参数必须使用双引号
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MxShop.settings')

# 安装django
django.setup()


class ImportCategoryData(object):
    """
    导入商品类目
    """
    def import_category_data(self, datas):
        from goods.models import GoodsCategory
        for data_lv1 in datas:
            goods_category_lv1 = GoodsCategory()
            goods_category_lv1.name = data_lv1['name']
            goods_category_lv1.code = data_lv1['code']
            goods_category_lv1.category_type = 1
            goods_category_lv1.save()

            for data_lv2 in data_lv1['sub_categorys']:
                goods_category_lv2 = GoodsCategory()
                goods_category_lv2.name = data_lv2['name']
                goods_category_lv2.code = data_lv2['code']
                goods_category_lv2.category_type = 2
                goods_category_lv2.parent_category = goods_category_lv1
                goods_category_lv2.save()

                for data_lv3 in data_lv2['sub_categorys']:
                    goods_category_lv3 = GoodsCategory()
                    goods_category_lv3.name = data_lv3['name']
                    goods_category_lv3.code = data_lv3['code']
                    goods_category_lv3.category_type = 3
                    goods_category_lv3.parent_category = goods_category_lv2
                    goods_category_lv3.save()


import_datas = ImportCategoryData()
import_datas.import_category_data(row_data)







