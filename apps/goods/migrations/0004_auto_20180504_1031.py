# Generated by Django 2.0.5 on 2018-05-04 02:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20180504_1029'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goods',
            old_name='good_brief',
            new_name='goods_brief',
        ),
    ]
