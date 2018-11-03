from functools import wraps
from django.shortcuts import redirect, reverse
from . import json_status
# from django.contrib.auth.decorators import login_required不能验证ajax的请求

def ajax_login_reruired(view_func):
    #自带的装饰器，保持函数原有的特性，例如函数名字
    @wraps(view_func)
    def warpper(request, *args, **kwargs):
        # 判断用户是否已登陆
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            # 判断是否是ajax请求
            if request.is_ajax():
                return json_status.params_error(message='请先登陆')
            else:
                return redirect(reverse('account:loading'))
    return warpper
