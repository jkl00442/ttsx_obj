# -*- coding:utf-8 -*-
from django.db import models
from df_goods.models import GoodsInfo

# Create your models here.
class CartInfo(models.Model):
    '''购物车'''
    #　谁买了多少个什么
    user = models.ForeignKey('df_user.UserInfo_2')
    goods = models.ForeignKey(GoodsInfo)
    count = models.IntegerField() # 整数
