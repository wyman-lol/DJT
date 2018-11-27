from django.http import Http404, JsonResponse
from django.shortcuts import render
from ..admin_staff.models import NewsTag
from ..news.models import News, NewsHot, NewsBanner
from .models import Course
import os, hmac, hashlib, time
from django.conf import settings



# Create your views here.
# 首页视图
def index_view(request):
    # news = News.objects.defer('content').select_related('tag', 'author').filter(is_delete=0).all()
    # 过滤掉content以及提前查询外健关联的tag、author
    news_tags = NewsTag.objects.filter(is_delete=0).all()
    newses = []
    for tag in news_tags:
        news = News.objects.filter(is_delete=0, tag=tag).all()[0:settings.ONE_PAGE_COUNT]
        if news:
            newses.append(news)
        else:
            newses.append(None)
    banners = NewsBanner.objects.filter(is_delete=False).all()
    h_news = NewsHot.objects.filter(is_delete=False).all()[0: 3]
    return render(request, 'course/index.html', context={
        'news_tags': news_tags,
        'newses': newses,
        'h_news': h_news,
        'banners': banners
    })
# 课程视图
def course(request):
    courses = Course.objects.filter(is_delete=False).all()
    return render(request, 'course/course.html', context={'courses': courses})

# 课程详情也
def course_detail(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        return render(request, 'course/course_detail.html', context={'course': course})
    except Course.DoesNotExist as info:
        raise Http404


# 百度云视频播放
def course_token(request):
    # 获取视频路径
    video_url = request.GET.get('video_url')
    # video_url = 'http://ih2vvidjmihrie7nvje.exp.bcevod.com/mda-ih6x46pcj8w9vbs1/mda-ih6x46pcj8w9vbs1.m3u8'
    # 过期时间
    expiration_time = int(time.time()) + 3600
    # 百度云 UserId / UserKey
    user_id = settings.BAIDU_CLOUD_USER_ID
    user_key = settings.BAIDU_CLOUD_USER_KEY

    # extension ===> .mu38
    extension = os.path.splitext(video_url)[1]
    # mda-ih6x46pcj8w9vbs1
    media_id = video_url.split('/')[-1].replace(extension, '')

    # key 和 message 转化为 bytes
    key = user_key.encode('utf-8')
    message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')
    # 加密盐 加密数据  加密方式
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{0}_{1}_{2}'.format(signature, user_id, expiration_time)
    return JsonResponse({"token": token})