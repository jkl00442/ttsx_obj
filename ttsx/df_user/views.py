# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from models import *
from hashlib import *
import datetime

# Create your views here.

def register(request):
    context = {'title': '注册'}
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

    # return HttpResponse('ok')
    return HttpResponseRedirect('/user/login/')

def check_name_2(request):
    name = request.GET.get('u_name')

    has = UserInfo_2.objects.filter(u_name = name).count()

    context = {'list':has}
    return JsonResponse(context)

def login(request):
    name = request.COOKIES.get('name', '')
    # if name is None:
    #     name = ''
    context = {'title': '登陆', 'name': name}
    return render(request, 'df_user/login.html', context)

def login_handle(request):
    dict = request.POST
    name = dict.get('username', '')
    pwd = dict.get('userpwd')
    remember = dict.get('remember_me','0') # 1 没有这个参数 默认为0

    print(remember)

    # 获取有没有这个用户名,有为[obj],没有为[]
    obj = UserInfo_2.objects.filter(u_name = name)

    print(obj)
    print(name)

    # if name is None:
    #     name = ''
    context = {'name':name}
    # 用长度来判断,如果用obj == []的话,下面再用obj[0]会出现索引超出范围异常
    if len(obj) == 0:
        # 没有这个用户名
        context['name_error'] = '1'
        print(context)
        return render(request, 'df_user/login.html', context)
    else:
        # 有这个用户名,来进行密码判断

        s1 = sha1()
        s1.update(pwd)
        pwd = s1.hexdigest()
        print(pwd)

        if obj[0].u_pwd == pwd:
            response = HttpResponseRedirect('/user/')
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

            return response
        else:
            # 密码错误
            context['pwd_error'] = '1'
            print(context)
            return render(request, 'df_user/login.html', context)


def index(request):
    context = {'title': '用户中心'}
    return render(request, 'df_user/user_center_info.html', context)

def test(request):
    return HttpResponse('ok')

# def user_center_info(request):
#     return render(request, 'df_user/user_center_info.html')
#
# def user_center_order(request):
#     return render(request, 'df_user/user_center_order.html')
#
# def user_center_site(request):
#     return render(request, 'df_user/user_center_site.html')
