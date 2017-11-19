# -*- coding:utf-8 -*-
from django.shortcuts import redirect

def user_login(fn):
    # 没有登陆不允许访问用户中心等地址

    def wrapper(request, *args, **kwargs):
        if request.session.has_key('u_id'):
            res = fn(request, *args, **kwargs)
            return res
        else:
            return redirect('/user/login/')

    return wrapper

