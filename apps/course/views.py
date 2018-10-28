from django.shortcuts import render
from ..admin_staff.models import NewsTag
from ..news.models import News


# Create your views here.

def index_view(request):
    # news = News.objects.defer('content').select_related('tag', 'author').filter(is_delete=0).all()
    # 过滤掉content以及提前查询外健关联的tag、author
    news_tags = NewsTag.objects.filter(is_delete=0).all()
    news = News.objects.filter(is_delete=0).all()
    return render(request, 'course/index.html', context={
        'news_tags': news_tags,
        'news': news
    })

def course(request):
    return render(request, 'course/course.html')