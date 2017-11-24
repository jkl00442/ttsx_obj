# -*- coding:utf-8 -*-

class UrlMiddleware(object):
    '''记录当前页面，登陆之后返回当前页面'''

    def process_view(self, request, view_func, view_args, view_kwargs):
        print(request.path)
        if request.path not in [
            '/user/register/',
            '/user/register_handle/',
            '/user/login/',
            '/user/login_handle/',
            '/user/logout/',
            '/user/order/',
            '/user/site/',
            '/user/recv_info/',
            '/user/is_login/',
            '/cart/add_cart/',
            '/cart/show_count/',
            '/cart/',
            '/cart/order/',
            # '/order/',
        ]:
            request.session['page_from'] = request.path

