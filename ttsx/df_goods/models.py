# -*- coding:utf-8 -*-
from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class TypeInfo(models.Model):
    title = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title.encode('utf-8')

class GoodsInfo(models.Model):
    # 写出商品字段
    # name, price, pic, 20.00/500g, title, content, 点击量, 库存, is_delete
    g_name = models.CharField(max_length=50)
    g_pic = models.ImageField(upload_to='goods')
    g_price = models.DecimalField(max_digits=5, decimal_places=2) # 999.99
    is_delete = models.BooleanField(default=False)
    g_unit = models.CharField(max_length=20)
    g_click = models.IntegerField(default=0)

    g_title = models.CharField(max_length=400)
    g_has = models.IntegerField(default=1000)

    g_content = HTMLField()

    g_type = models.ForeignKey(TypeInfo)

