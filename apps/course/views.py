from django.shortcuts import render
from ..admin_staff.models import NewsTag
from ..news.models import News
from django.conf import settings


# Create your views here.

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
    return render(request, 'course/index.html', context={
        'news_tags': news_tags,
        'newses': newses
    })

def course(request):
    return render(request, 'course/course.html')