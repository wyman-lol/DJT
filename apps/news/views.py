from django.shortcuts import render, Http404
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from utils import json_status
import os
from DJT import settings
from .forms import NewsPubForm
from ..admin_staff.models import NewsTag
from .models import News

# 发布新闻页面
@method_decorator([csrf_exempt, staff_member_required(login_url='/account/loading/')], name='dispatch')
class NewsPUbView(View):
    def get(self, request):
        tags = NewsTag.objects.filter(is_delete=0).all()
        return render(request, 'news/newspub.html', context={'tags': tags})

    def post(self, request):
        form = NewsPubForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            tag_id = form.cleaned_data.get('tag_id')
            photo_url = form.cleaned_data.get('photo_url')
            content = form.cleaned_data.get('content')
            tag = NewsTag.objects.filter(id=tag_id).first()
            if tag:
                News.objects.create(title=title, desc=desc, tag=tag, photo_url=photo_url, content=content,
                                    author=request.user)
                return json_status.result()
        else:
            return json_status.params_error(message=form.get_error())

# 上传文件
@csrf_exempt
def UploadFile(request):
    file = request.FILES.get('upload_file')
    file_name = file.name
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    print(file)
    with open(file_path, 'wb') as data:
        # chunks 返回一个生成器
        for chunk in file.chunks():
            data.write(chunk)
    # 返回当前视图的绝对路径http://127.0.0.1:8000/admin/upload-file/
    # http: // 127.0.0.1: 8000 / Users / luweimin / PycharmProjects / DJT / mediacode.md
    file_url = request.build_absolute_uri(settings.MEDIA_URL + file_name)
    return json_status.result(data={'file_url': file_url})

# 新闻详情页面
def news_detail(request, news_id):
    # news = News.objects.filter(id=news_id, is_delete=0).first()
    # return render(request, 'news/news_detail.html', context={'news': news, })
    try:
        news = News.objects.get(id=news_id, is_delete=0)
        return render(request, 'news/news_detail.html', context={'news': news, })
    except News.DoesNotExist:
        # 页面不存在或者说找不到新闻，跑村http404错误,只能debug=false才能用
        raise Http404