# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0002_auto_20171105_1240'),
        ('df_goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('o_count', models.IntegerField(default=0)),
                ('o_price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('o_goods', models.ForeignKey(to='df_goods.GoodsInfo')),
            ],
        ),
        migrations.CreateModel(
            name='OrderMain',
            fields=[
                ('order_id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('o_date', models.DateTimeField(auto_now=True)),
                ('o_status', models.IntegerField(default=0)),
                ('o_total', models.DecimalField(max_digits=7, decimal_places=2)),
                ('o_user', models.ForeignKey(to='df_user.UserInfo_2')),
            ],
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='o_main',
            field=models.ForeignKey(to='df_order.OrderMain'),
        ),
    ]
