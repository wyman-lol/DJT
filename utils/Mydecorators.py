from functools import wraps
from django.contrib.auth.models import ContentType, Permission
from django.shortcuts import redirect, reverse
from . import json_status


# from django.contrib.auth.decorators import login_required不能验证ajax的请求

def ajax_login_reruired(view_func):
    # 自带的装饰器，保持函数原有的特性，例如函数名字
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


# 权限相关的装饰器
def user_permission_required(model_name):
    def wrapper(view_func):
        @wraps(view_func)
        def func(request, *args, **kwargs):
            # 根据对应的模型找到 对应的content_type
            content_type = ContentType.objects.get_for_model(model_name)
            # 找到权限
            permissions = Permission.objects.filter(content_type=content_type)
            # 拼接权限 app名字.权限名字 ==> news.change_news
            code_name = [content_type.app_label + '.' + permission.codename for permission in permissions]
            # 判断是否具有权限
            print(code_name)
            res = request.user.has_perms(code_name)
            if res:
                return view_func(request, *args, **kwargs)
            return json_status.un_auth_error(message='权限不足')

        return func

    return wrapper


def is_super_user_required(fun):
    @wraps(fun)
    def wrapper(request, *agrs, **kwargs):
        if request.user.is_superuser:
            return fun(request, *agrs, **kwargs)
        else:
            return json_status.un_auth_error(message='权限不足，需要超级管理员权限')
    return wrapper
