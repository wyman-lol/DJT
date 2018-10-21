from django import forms
from utils import Mymemcache


class LoginForm(forms.Form):
    telephone = forms.CharField(max_length=11, min_length=11,
                                error_messages={'min_length': '手机号码长度有误', 'max_length': '手机号码长度有误',
                                                'required': '手机号码不能为空'})
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={'min_length': '密码小于六位数', 'max_length': '密码大于20位数', 'required': '密码不能为空'})
    remember = forms.BooleanField(required=False)


class RegisterForm(forms.Form):
    telephone = forms.CharField(max_length=11, min_length=11,
                                error_messages={'min_length': '手机号码长度有误', 'max_length': '手机号码长度有误',
                                                'required': '手机号码不能为空'})
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={'min_length': '密码小于六位数', 'max_length': '密码大于20位数', 'required': '密码不能为空'})
    repeat_password = forms.CharField(max_length=20, min_length=6,
                                      error_messages={'min_length': '密码小于六位数', 'max_length': '密码大于20位数',
                                                      'required': '密码不能为空'})
    sms_captcha = forms.CharField(max_length=6, min_length=6,
                              error_messages={'min_length': '请输入六位数验证码', 'max_length': '请输入六位数验证码',
                                              'required': '短信验证码不能为空'})
    username = forms.CharField(max_length=16, min_length=2,
                                      error_messages={'min_length': '用户名小于两位数', 'max_length': '用户名大于16位数',
                                                      'required': '用户名不能为空'})
    graph_captcha = forms.CharField(max_length=4, min_length=4,
                                  error_messages={'min_length': '请输入4位数验证码', 'max_length': '请输入4位数验证码',
                                                  'required': '图片验证码不能为空'})
    # 判断密码、验证码、短信验证码
    def check_data(self):
        # 两次密码不一致，给forms的password添加错误
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        if password != repeat_password:
            return self.add_error('sms_captcha', '两次密码不一致')

        # 短信验证码不一致，给forms的password添加错误
        sms_captcha = self.cleaned_data.get('sms_captcha')
        telephone = self.cleaned_data.get('telephone')
        sms_send = Mymemcache.get_key(telephone)
        if sms_send and sms_send == sms_captcha:
            pass
        else:
            return self.add_error('sms_captcha', '短信验证码错误')

        # 图片验证码不一致，给forms的password添加错误
        graph_captcha = self.cleaned_data.get('graph_captcha').lower()
        graph_memcache = Mymemcache.get_key(graph_captcha)
        if graph_memcache and graph_captcha == graph_memcache.lower():
            pass
        else:
            return self.add_error('sms_captcha', '图片验证码错误，请点击刷新')

        return True