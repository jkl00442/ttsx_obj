# -*- coding:utf-8 -*_
from django.db import models
from df_user.models import UserInfo_2
from df_goods.models import GoodsInfo

# Create your models here.
class OrderMain(models.Model):
    '''订单数据主表'''
    # 订单id,用户id，订单创建日期,订单状态，订单金额
    order_id = models.CharField(max_length=20, primary_key=True) # 主键,2017 11 19 13 41 30 u_id
    o_user = models.ForeignKey(UserInfo_2) # 哪个用户
    o_date = models.DateTimeField(auto_now=True) # 数据行创建时自动生成日期时间
    o_status = models.IntegerField(default=0)
    o_total = models.DecimalField(max_digits=7, decimal_places=2, default=0)

class OrderDetail(models.Model):
    '''订单数据从表'''
    # 订单中的一个商品，数量,单价
    o_main = models.ForeignKey(OrderMain)
    o_goods = models.ForeignKey(GoodsInfo)
    o_count = models.IntegerField(default=0)
    o_price = models.DecimalField(max_digits=5, decimal_places=2)
