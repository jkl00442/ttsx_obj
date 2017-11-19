# -*- coding:utf-8 -*-

from haystack import indexes
from models import *

class GoodsInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return GoodsInfo #　对那个类建立索引

    def index_queryset(self, using=None):
        return self.get_model().objects.all() # 获取这张表的哪些(哪几行)数据