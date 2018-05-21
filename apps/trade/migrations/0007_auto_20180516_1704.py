# Generated by Django 2.0.5 on 2018-05-16 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0006_auto_20180516_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='goods.Goods', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.OrderInfo', verbose_name='所属订单'),
        ),
        migrations.AlterField(
            model_name='ordershoppingcart',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.OrderInfo', verbose_name='所属订单'),
        ),
        migrations.AlterField(
            model_name='ordershoppingcart',
            name='shopping_cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_cart', to='trade.ShoppingCart', verbose_name='所属购物车'),
        ),
    ]
