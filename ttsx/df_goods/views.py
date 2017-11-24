# -*- coding:utf-8 -*-
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator, Page
from datetime import date
from haystack.generic_views import SearchView

# Create your views here.
def index(request):
    goods_list = [] #[{'type', 'name', 'price', 'pic'}, {}, {}, {}]  # [{type:'', goods:[obj, obj, obj, obj]}, {}, {}]

    # 获取分类对象列表
    type_list = TypeInfo.objects.all()

    for i in type_list:
        n_goods = i.goodsinfo_set.order_by('-id')[:4] # 获取分类对象goosdinfo子表,并对所有数据进行排序(降序)
        c_goods = i.goodsinfo_set.order_by('-g_click')[:4]
        goods_list.append({'type': i, 'n_goods': n_goods, 'c_goods': c_goods})

    # num = len(type_list[0].goodsinfo_set.order_by('id')) # 拿到了30个数据
    # print(num)

    # print(goods_list)

    # 获取分类对象列表
    # 每个分类中所对应的4个最新商品,4个最火商品
    context = {'goods_list': goods_list, 'title': '首页', 'top_search': '0'}
    return render(request, 'df_goods/index.html', context)

def list(request, t_id, p_index, order_b):

    p_index = int(p_index)
    order_b = int(order_b)
    # 获取传过来的分类id
    # 根据分类id获取分类对象
    try:
        type_obj = TypeInfo.objects.get(id=int(t_id))

        order_str = '-id' # 默认排序

        desc = '0'

        if order_b == 2: # 价格排序
            desc = request.GET.get('desc', '0')
            if desc == '1':
                order_str = '-g_price'
            else:
                order_str = 'g_price'

        elif order_b == 3: # 点击量排序
            order_str = '-g_click'

        # 获取分类对象子表的所有数据--->all()或order_by()
        goods_list = type_obj.goodsinfo_set.order_by(order_str)

        n_goods_list = type_obj.goodsinfo_set.order_by('-id')[:2] # 2个新品

        # 对得到的所有数据进行分页
        page_list = Paginator(goods_list, 15) # 得到分页对象

        # 对超出范围的页码进行处理
        if p_index < 1:
            p_index = 1
        elif p_index > page_list.num_pages:
            p_index = page_list.num_pages

        goods_list = page_list.page(p_index) # 获取第几页
            # page_list.page_range() # 返回页码列表


        context = {'title': '商品列表', 'top_search': '0', 'goods_list': goods_list, 't_o': type_obj, 'n_goods':
            n_goods_list, 'p_index': p_index, 'order_b': order_b, 'desc': desc}
        return render(request, 'df_goods/list.html', context)
    except Exception as e:
        return render(request, '404.html')

def detail(request, g_index):
    # 获取url匹配到的商品id

    try:
        # 查找这个id对象,并传到模板中去
        goods_obj = GoodsInfo.objects.get(id = int(g_index)) # 商品对象

        # 根据这个id找到对应的分类信息
        # type_obj = TypeInfo.objects.get(goodsinfo__id = g_index) # 分类对象
        # 根据这个分类对象查找到最新的2件商品
        # n_goods_list = type_obj.goodsinfo_set.order_by('-id')[:2]

        # 或
        # 或  根据这个id查找到对应的分类对象,并获取这个分类对象所对应的两个最新商品
        type_obj = goods_obj.g_type
        n_goods_list = type_obj.goodsinfo_set.order_by('-id')[:2]

        # 点击量加1
        goods_obj.g_click += 1
        goods_obj.save()

        context = {'title': '商品详情', 'top_search': '0', 'type': type_obj, 'goods': goods_obj, 'n_goods': n_goods_list}

        response = render(request, 'df_goods/detail.html', context)

        # 给用户添加浏览历史
        # 每当用户浏览商品页,给他添加一条此商品信息
        # 先获取以后的浏览记录,浏览记录保持在5条
        look_list = request.COOKIES.get('look_ids', '').split(',') # 对获取到的look_ids进行拆分成列表
        print(look_list)
        if look_list[-1] == '':
            look_list.pop()
        print(look_list)

        # 如果这个商品的记录重复存在,删除,并把它移到最新的位置
        if g_index in look_list:
            look_list.remove(g_index)

        look_list.insert(0, g_index)
        # 将浏览记录保持在5个
        if len(look_list) > 5:
            look_list.pop()

        print(look_list)
        # 能根据浏览记录回到此商品页
        response.set_cookie('look_ids', ','.join(look_list), max_age=60*60*24*7)

        return response
    except Exception as e:
        return render(request, '404.html')

class MySearchView(SearchView):
    """My custom search view."""
    # 全文检索自定义视图

    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        context['title'] = '搜索结果'
        context['top_search'] = '0'
        page_list = []
        page = context.get('page_obj')
        if page.paginator.num_pages < 5: #　不足５页
            page_list = page.paginator.page_range
        # 大于五页
        elif page.number <= 2: # 当显示页为１，２页时
            page_list = range(1, 6)
        elif page.number >= (page.paginator.num_pages - 1):
            page_list = range(page.paginator.num_pages-4 ,page.paginator.num_pages+1)
        else:
            page_list = range(page.number-2, page.number+3)

        context['page_list'] = page_list
        print(page_list)
        return context

