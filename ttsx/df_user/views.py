# -*- coding:utf-8 -*-
import datetime
from hashlib import *

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from user_decorators import *
from df_goods.models import *
from df_order.models import *
from django.core.paginator import Paginator

from models import *


# Create your views here.

def register(request):
    context = {'title': '注册', 'top': '1'}

    return render(request, 'df_user/register.html', context)

def register_handle(request):
    dict = request.POST
    name = dict.get('user_name')
    pwd = dict.get('pwd')
    email = dict.get('email')

    s = sha1()
    pwd = s.update(pwd)
    u_pwd = s.hexdigest()
    print(u_pwd)

    # 一条数据插入两张相关联的表(一对多的一)
    u = UserInfo_2()
    u.u_name = name
    u.u_pwd = u_pwd
    u.save()

    # 一条数据插入两张相关联的表(一对多的多)
    addr = UserAddress_2()
    addr.u_info = u
    addr.u_email = email
    addr.save()


    return HttpResponseRedirect('/user/login/')

def check_name_2(request):
    name = request.GET.get('u_name')

    has = UserInfo_2.objects.filter(u_name = name).count()

    context = {'list':has}
    return JsonResponse(context)

def login(request):
    name = request.COOKIES.get('name', '')

    context = {'title': '登陆', 'name': name, 'top': '1'}

    return render(request, 'df_user/login.html', context)

def login_handle(request):
    dict = request.POST
    name = dict.get('username', '')
    pwd = dict.get('userpwd')
    remember = dict.get('remember_me','0') # 1 没有这个参数 默认为0

    # print(remember)

    # 获取有没有这个用户名,有为[obj],没有为[]
    obj = UserInfo_2.objects.filter(u_name = name)

    # print(obj)
    # print(name)

    # if name is None:
    #     name = ''
    context = {'name':name, 'top': '1', 'title': '登陆'}
    # 用长度来判断,如果用obj == []的话,下面再用obj[0]会出现索引超出范围异常
    if len(obj) == 0:
        # 没有这个用户名
        context['name_error'] = '1'
        # print(context)
        return render(request, 'df_user/login.html', context)
    else:
        # 有这个用户名,来进行密码判断

        s1 = sha1()
        s1.update(pwd)
        pwd = s1.hexdigest()
        print(pwd)

        if obj[0].u_pwd == pwd:
            page_from = request.session.get('page_from', '/user/')
            response = HttpResponseRedirect(page_from)
            # 密码正确
            if remember == '1':
                # 记住用户名

                # 设置cookie过期时间,两周
                now = datetime.datetime.now()
                two_weeks = datetime.timedelta(days=14)
                expire_day = now + two_weeks

                response.set_cookie('name', name, expires = expire_day)
            else:
                # 不记住用户名
                response.delete_cookie('name')


            request.session['u_id'] = obj[0].id
            request.session['u_name'] = obj[0].u_name
            # print(obj[0].id)

            return response


        else:
            # 密码错误
            context['pwd_error'] = '1'
            print(context)
            return render(request, 'df_user/login.html', context)

def logout(request):
    page_from = request.session.get('page_from', '/user/login/')
    request.session.flush()

    return HttpResponseRedirect(page_from)

def is_login(request):
    # 判断用户是否登陆
    # 获取session中的u_id，如果有，证明已登录, 没有，则说明没有登陆
    res = request.session.get('u_id')
    print(res)
    if res:
        return JsonResponse({'res': 1})
    else:
        return JsonResponse({'res': 0})


@user_login
def user(request):


    list = UserInfo_2.objects.filter(id=request.session['u_id']) # 列表[obj, obj, ...]

    # 获取list[0]的所有子表
    # print(list[0].useraddress_2_set.all()[0].u_email)
    # print(type(list[0].useraddress_2_set.all()[0].u_email))

    email = list[0].useraddress_2_set.all()[0].u_email
    print(email)

    # 读取cookie中存取的浏览记录,并把它们填充到模板中去
    look_list = request.COOKIES.get('look_ids', '').split(',') # str--->list
    look_list_2 = []
    if look_list[-1] == '':
        look_list.pop()

    else:
        for i in look_list:
            obj = GoodsInfo.objects.get(id=int(i))
            look_list_2.append(obj)


    context = {'title': '用户中心', 'user': list[0], 'email': email, 'look_list': look_list_2}

    return render(request, 'df_user/center.html', context)

@user_login
def order(request):
    p_index = request.GET.get('p_index', '1')

    order_list = OrderMain.objects.filter(o_user_id=request.session.get('u_id')) #　查询用户的所有订单
    order_page = Paginator(order_list, 2)
    o_page = order_page.page(int(p_index))

    all_page_list = []

    if o_page.paginator.num_pages < 5: #　小于5页
        all_page_list = o_page.paginator.page_range

    # 大于5页
    elif o_page.num <= 2:
        all_page_list = range(1, 6)

    elif o_page.num >= (o_page.paginator.num_pages - 1):
        all_page_list = range((o_page.paginator.num_pages - 4), (o_page.paginator.num_pages + 1))

    else:
        all_page_list = range(o_page.number - 2, o_page.number + 2)

    context = {'title': '全部订单', 'order_list': o_page, 'all_page_list': all_page_list, 'p_index': p_index}
    return render(request, 'df_user/order.html', context)

@user_login
def site(request):

    list = UserInfo_2.objects.filter(id=request.session['u_id']) # 列表 [obj, obj, ...]

    user_addr = list[0].useraddress_2_set.all()
    # print(user_addr)
    # print(type(user_addr))
    print(user_addr[0].u_zip)
    print(user_addr[0].u_address)

    context = {'user': list[0], 'user_addr': user_addr[0], 'title': '收货地址'}

    return render(request, 'df_user/site.html', context)

@user_login
def recv_info(request):
    # 获取要修改的这个用户对象
    list = UserInfo_2.objects.get(id=request.session.get('u_id')) # 列表[obj, obj, ...]


    dict = request.POST
    name = dict.get('recv_name')
    addr = dict.get('recv_addr')
    zip = dict.get('recv_zip')
    phone = dict.get('recv_phone')

    print('%s,,%s,,%s,,%s'%(name, addr, zip, phone))

    user_add = UserAddress_2()
    user_add.u_info = list # 获取于这个对象关联的子表

    # 为这个对象写入数据
    list.u_phone = phone

    user_add.u_get = name
    user_add.u_address = addr
    user_add.u_zip = zip

    # 保存更改
    user_add.save()
    list.save()

    return HttpResponseRedirect('/user/site/')

def test(request):
    pass
