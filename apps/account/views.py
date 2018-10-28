from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from .form import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from utils.captcha.captcha import Captcha
from utils.aliysms.sms_send import send_sms
from io import BytesIO
from utils import Mymemcache
import random
from .models import User
# Create your views here.
# 不启用跨域请求拦截
@method_decorator([csrf_exempt, ], name='dispatch')
class LoginView(View):
    def get(self, request, *agrs, **kwargs):
        return render(request, 'account/loading.html')

    def post(self, request, *agrs, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone', None)
            password = form.cleaned_data.get('password', None)
            remember = form.cleaned_data.get('remember', None)
            print(telephone,password)
            user = authenticate(username=telephone, password=password)
            if user:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    pass
                return JsonResponse({"code": 1, "msg": "登录成功", "data": "xxx"})
            else:
                return JsonResponse({"code": 2, "msg": "手机或密码错误", "data": "xxx"})
        else:
            # 去掉字典最后一项并返回
            msg = form.errors.popitem()[1][0]
            return JsonResponse({"code": 2, "msg": msg, "data": "xxx"})
# 注册
@method_decorator([csrf_exempt, ], name='dispatch')
class RegisterView(View):
    def get(self, request, *agrs, **kwargs):
        return render(request, 'account/register.html')
    def post(self, request, *agrs, **kwargs):
        # 因为不是用{{ forms_as }}所以要把request传进实例判断
        form = RegisterForm(request.POST)
        if form.is_valid() and form.check_data():
            # 注册用户到数据库
            telephone = form.cleaned_data.get('telephone')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(telephone=telephone)
            # 判断用户是否已存在
            if user:
                return JsonResponse({"code": 1, "msg": "此手机号以注册", "data": "xxx"})
            else:
                user = User.objects.create_user(telephone=telephone, username=username, password=password)
                # 保存用户登陆状态，提高用户体验
                login(request, user)
                return JsonResponse({"code": 2, "msg": "注册成功", "data": "xxx"})
        msg = form.errors.popitem()[1][0]
        return JsonResponse({"code": 1, "msg": msg, "data": "xxx"})

# 图片验证码
def graph_chptcha(request):
    # 获取验证码
    text, img = Captcha.gene_code()
    # 保存图片为二进制,字节流
    photo = BytesIO()
    img.save(photo, 'png')
    photo.seek(0)
    Mymemcache.set_key(text.lower(), text.lower(), time=60*10)
    # 设置一个httpresponse返回图片
    result = HttpResponse(content_type='image/png')
    # 写入图片
    result.write(photo.read())
    return result

# 发送短信验证码
def sms_send(request):
    telphone = request.GET.get('telphone')
    captcha = str(random.randint(100000, 999999))
    # 发送短信
    # result = send_sms(telphone, captcha)
    # 把用户和验证码存入缓存
    Mymemcache.set_key(telphone, captcha, time=60*3)
    print(telphone, captcha)
    # print(result)
    return HttpResponse('<h3>success</h3>')

# 退出
def LogoutView(request):
    logout(request)
    return redirect(reverse('account:loading'))





