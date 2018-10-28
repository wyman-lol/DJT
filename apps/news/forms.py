from django import forms
from apps.forms import FormMixin

class NewsPubForm(forms.Form, FormMixin):
    title = forms.CharField(max_length=100, min_length=2, error_messages={'required':'新闻标题不能为空', 'max_length':'新闻标题字数不能大于100'})
    desc = forms.CharField(max_length=200, min_length=2, error_messages={'required':'新闻标题不能为空', 'max_length':'新闻标题字数不能大于200'})
    tag_id = forms.IntegerField(error_messages={'required': 'ID不能为空'})
    photo_url = forms.CharField(error_messages={'required': '图片不能为空'})
    content = forms.CharField(max_length=10000, min_length=2, error_messages={'required':'新闻内容不能为空', 'max_length':'内容不能超过10000'})