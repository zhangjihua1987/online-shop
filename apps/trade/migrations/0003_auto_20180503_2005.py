# Generated by Django 2.0.5 on 2018-05-03 12:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_goodscategorybrand_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trade', '0002_auto_20180503_1840'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShopCart',
            new_name='ShoppingCart',
        ),
    ]
