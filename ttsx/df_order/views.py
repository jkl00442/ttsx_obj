# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import transaction
from models import *
from datetime import datetime
from df_cart.models import *

# Create your views here.
def order_handle(request):
    ok = False
    # 创建保存点,保存点到提交或回滚之间的操作会保存到本地
    sid = transaction.savepoint()

    try:
        # 创建订单
        order = OrderMain() # 新建对象(用类)

        # 生成订单id
        order_time = datetime.now().strftime('%Y%m%d%H%M%S')
        u_id = request.session.get('u_id')

        # 订单主表
        order.order_id = '%s%s'%(order_time, u_id)
        order.o_user_id = u_id
        order.save()

        # 获取购物车id，再从购物车中查到用户id对应着的商品id
        # 用户订单中所对应的购物车数据
        cart_id_list = request.POST.get('get_ids').split(',') # ['', '', '', ]
        cart_list = CartInfo.objects.filter(id__in=cart_id_list)
        # 从购物车表中获取这条订单记录，写入订单表

        total_all = 0

        # 判断库存是否足够用户购买，够，减库存
        for i in cart_list:
            if i.count <= i.goods.g_has:
                detail = OrderDetail() # 在从表中创建多行数据，新建对象(用类)
                detail.o_main = order
                detail.o_goods_id = i.goods_id
                detail.o_count = i.count
                detail.o_price = i.goods.g_price

                detail.save()

                # 修改库存数量
                i.goods.g_has -= i.count
                i.goods.save()

                # 计算总金额
                total = i.goods.g_price*i.count
                total_all += total

                i.delete() #　从购物车表中删除这些数据
                ok = True
            else:
                transaction.savepoint_rollback(sid)
                break

        if ok:

            order.o_total = total_all
            order.save()
            # 提交
            transaction.savepoint_commit(sid)

    except Exception as e:
        print(e)
        transaction.savepoint_rollback(sid)
        # 回滚
        ok = False

    if ok:
        return HttpResponseRedirect('/user/order/')
    else:
        return HttpResponseRedirect('/cart/')
