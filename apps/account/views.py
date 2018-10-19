from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from .form import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from utils.captcha.captcha import Captcha
from io import BytesIO
from utils import Mymemcache
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

# 登陆
class RegisterView(View):
    def get(self, request, *agrs, **kwargs):
        return render(request, 'account/register.html')
# 退出
def LogoutView(request):
    logout(request)
    return redirect(reverse('account:loading'))

def graph_chptcha(request):
    # 获取验证码
    text, img = Captcha.gene_code()
    # 保存图片为二进制,字节流
    photo = BytesIO()
    img.save(photo, 'png')
    photo.seek(0)
    # 设置一个httpresponse返回图片
    result = HttpResponse(content_type='image/png')
    result.write(photo.read())
    return result








