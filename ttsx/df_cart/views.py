# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from models import *
from df_user.models import *
from df_goods.models import GoodsInfo
from df_user.user_decorators import *
from django.db.models import Sum

# Create your views here.
# def list(request):
#     # 获取传过来的商品id
#     # 把用户的购物车信息保存
#     # 返回用户购物车数量?还是说在jquery中做
#     g_id = request.GET.get('g_id')
#     print(g_id)
#     goods_list = request.session.get('goods_list', [])
#     goods_list.insert(0, g_id)
#     print(goods_list)
#     request.session['goods_list'] = goods_list
#
#     return JsonResponse({'count':len(goods_list)})

# def detail(request):
#     g_id = request.GET.get('g_id')
#     num = request.GET.get('num')
#
#     goods_list = request.session.get('goods_list', [])
#     for i in range(int(num)):
#         goods_list.insert(0, g_id)
#         print('111')
#
#     print(goods_list)
#     request.session['goods_list'] = goods_list
#
#     context = {}
#     return JsonResponse(context)

def add_cart(request):
    # 获取传来的商品id,数量
    # 把这些用户，购物车信息(id, count)写入表中

    try:
        g_id = int(request.GET.get('g_id'))
        g_count = int(request.GET.get('count', '1'))

        # obj_list = CartInfo.objects.filter(user=request.session['u_id']).filter(goods=g_id) #　外键或外键写在表中所对应的字段名都可以
        obj_list = CartInfo.objects.filter(user_id = request.session['u_id'], goods_id = g_id)
        if len(obj_list) == 1:
            obj_list[0].count += g_count
            obj_list[0].save()

        else:
            cart = CartInfo()

            cart.user_id = request.session.get('u_id')
            cart.goods_id = g_id
            cart.count = g_count

            cart.save()

        context = {'ok':1}
        return JsonResponse(context)

    except Exception as e:
        print(e)
        context = {'ok':0}
        return JsonResponse(context)

def show_count(request):
    # 获取用户id,根据id查询所有加入购物车的商品数量
    u_id = request.session['u_id']
    # get_count = CartInfo.objects.flter(user_id = u_id).aggregate(Sum('count'))
    # print(get_count)
    obj_list = CartInfo.objects.filter(user_id = u_id)
    num = 0
    for i in obj_list:
        num +=i.count

    print(num)

    context = {'count': num}
    return JsonResponse(context)

def index(request):
    u_id = request.session['u_id']
    obj_list = CartInfo.objects.filter(user_id = u_id)
    context = {'title': '购物车', 'list': obj_list}
    return render(request, 'df_cart/cart.html', context)

def edit(request):
    id = request.GET.get('id')
    count = request.GET.get('count')

    obj = CartInfo.objects.get(id=id)
    obj.count = count

    obj.save()

    context = {'ok': 1}
    return JsonResponse(context)

def delete_cart(request):
    id = request.GET.get('id')
    print(id)
    print(type(id))

    obj = CartInfo.objects.get(id=id).delete()

    context = {'ok': 1}
    return JsonResponse(context)

def order(request):
    # 获取用户id
    u_id = request.session.get('u_id')
    user = UserInfo_2.objects.get(pk=u_id)

    # 获取用户所有收件人信息
    addr_list= UserAddress_2.objects.filter(u_info_id=u_id)

    # 获取用户购物车商品信息
    id_list = request.POST.getlist('cart_id') # [u'21', u'22']
    cart_list = CartInfo.objects.filter(id__in=id_list)
    ids = ','.join(id_list)
    print(ids)

    # 传到支付页面
    context = {'title': '提交订单', 'user': user, 'addr_list': addr_list, 'cart_list': cart_list, 'ids': ids}
    return render(request, 'df_cart/order.html', context)
