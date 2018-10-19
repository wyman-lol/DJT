from django import forms


class LoginForm(forms.Form):
    telephone = forms.CharField(max_length=11, min_length=11,
                                error_messages={'min_length': '手机号码长度有误', 'max_length': '手机号码长度有误','required': '手机号码不能为空'})
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={'min_length': '密码小于六位数', 'max_length': '密码大于20位数', 'required': '密码不能为空'})
    remember = forms.BooleanField(required=False)


class RegisterForm(forms.Form):
    pass