from django.http import QueryDict
from django.shortcuts import render
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from utils import json_status
from utils.Mydecorators import user_permission_required
from .models import NewsTag
from ..news.models import News
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from DJT import settings
from urllib.parse import urlencode
from django.utils.timezone import make_aware
from ..news.forms import NewsHotAddForm, NewsEditForm
from ..news.models import NewsHot


# Create your views here.
def staff(request):
    return render(request, 'admin_staff/index/index.html')


# 装饰器去掉跨域验证，检验是否是员工账号登陆，不是的话去到登陆页面，next=管理页面
@method_decorator([csrf_exempt, staff_member_required(login_url='/account/loading/')], name='dispatch')
class NewsTagView(View):
    def get(self, request):
        news_tag = NewsTag.objects.filter(is_delete=False).all()
        return render(request, 'admin_staff/news/news_manage.html', context={'news_tag': news_tag, })

    # 新增标签
    def post(self, request):
        name = request.POST.get('name')
        if name.strip():
            # exists存在就返回true不存在就返回false
            tag_exists = NewsTag.objects.filter(tag_name=name).exists()
            if tag_exists:
                return json_status.params_error('标签已存在')
            else:
                NewsTag.objects.create(tag_name=name)
                return json_status.ok()
        else:
            return json_status.params_error('标签已存在')

    # 修改、编辑标签
    def put(self, request):
        # request的内容都在body里面，把body转换为query字典
        result = QueryDict(request.body)
        tag_name = result.get('tag_name')
        tag_id = result.get('tag_id')
        if tag_name and tag_id:
            tag = NewsTag.objects.filter(tag_name=tag_name).exists()
            if tag:
                return json_status.params_error('标签已存在')
            else:
                tag = NewsTag.objects.filter(id=tag_id)
                tag.update(tag_name=tag_name)
                return json_status.result()
        else:
            return json_status.params_error('请输入正确标签')

    # 删除标签
    def delete(self, request):
        result = QueryDict(request.body)
        tag_id = result.get('tag_id')
        tag = NewsTag.objects.filter(id=tag_id)
        if tag:
            tag.update(is_delete=True)
            return json_status.ok()
        else:
            return json_status.params_error('标签已删除或不存在')


# 新闻管理
@method_decorator([csrf_exempt, ], name='dispatch')
class NewsMasterView(View):
    def get(self, request):
        newses = News.objects.defer('content').select_related('tag', 'author').filter(is_delete=False)
        p = int(request.GET.get('p', 1))
        start_time = request.GET.get('start_time', '')
        end_time = request.GET.get('end_time', '')
        title = request.GET.get('title', '')
        author = request.GET.get('author', '')
        tag_id = request.GET.get('tag_id', 0)
        # 后台返回新闻标题到前端，避免每次点击查询时候标签栏都会清空

        if start_time and end_time:
            start_time_1 = datetime.strptime(start_time, '%Y/%m/%d')
            end_time_1 = datetime.strptime(end_time, '%Y/%m/%d') + timedelta(days=1)
            # make_aware消除时区设置后的报错问题
            newses = newses.filter(add_time__range=(make_aware(start_time_1), make_aware(end_time_1)))
        if title:
            # contains。。。包含title
            newses = newses.filter(title__icontains=title)
        if author:
            newses = newses.filter(author__username__icontains=author)
        if int(tag_id) > 0:
            newses = newses.filter(tag_id=tag_id)
        # 分页，每页2条新闻
        one_page_news = Paginator(newses, settings.ONE_PAGE_COUNT)
        # 返回第p页的新闻，pages.object_list新闻数据
        pages = one_page_news.page(p)
        news_tag = NewsTag.objects.filter(is_delete=False).all()
        context = {'newses': pages.object_list,
                   'news_tag': news_tag,
                   'page': pages,
                   'paginator': one_page_news,
                   'start_time': start_time,
                   'end_time': end_time,
                   'title': title,
                   'author': author,
                   'tag_id': int(tag_id),
                   'url_param': urlencode({  # urlecode把参数转化为key=value的形式
                       'start_time': start_time,
                       'end_time': end_time,
                       'title': title,
                       'author': author,
                       'tag_id': tag_id,
                   })
                   }
        page_data = NewsMasterView.get_page_data(one_page_news, pages)
        context.update(page_data)
        return render(request, 'admin_staff/news/news_master.html', context=context)

    # 静态方法，相当于全局函数，不用实例化就可以调用，调用时候不会自动把实例传给方法，因为没有self
    # 分页优化
    @staticmethod
    def get_page_data(paginator, page, around_count=2):
        # 当前页码
        current_page = page.number
        # 总页数
        total_page = paginator.num_pages

        left_has_more = False
        right_has_more = False
        # 左边页码区间
        left_start_index = current_page - around_count
        left_end_index = current_page

        if current_page < around_count + around_count + 1:
            left_page = range(1, left_end_index)
        else:
            left_has_more = True
            left_page = range(left_start_index, left_end_index)
        # 右边页码区间
        right_start_index = current_page + 1
        right_end_index = current_page + around_count + 1
        if current_page >= total_page - around_count - 1:
            right_page = range(right_start_index, total_page + 1)
        else:
            right_has_more = True
            right_page = range(right_start_index, right_end_index)

        return {'current_page': current_page,
                'total_page': total_page,
                'left_has_more': left_has_more,
                'left_page': left_page,
                'right_has_more': right_has_more,
                'right_page': right_page
                }

    # 删除新闻
    def delete(self, request):
        from django.http import QueryDict
        res = QueryDict(request.body)
        news_id = res.get('news_id')
        if news_id:
            news = News.objects.filter(id=news_id).first()
            if news:
                hot_news = NewsHot.objects.filter(news=news)
                if hot_news:
                    hot_news.update(is_delete=True)
                news.is_delete = True
                news.save()
                return json_status.result()
            return json_status.params_error(message="新闻不存在")
        return json_status.params_error(message="参数错误")


# 热门新闻管理，编辑和删除
@method_decorator(csrf_exempt, name='dispatch')
class NewsHotView(View):
    def get(self, request):
        return render(request, 'news/news_hot.html')

    def put(self, request):
        ret = QueryDict(request.body)
        priority = int(ret.get('priority', 0))
        if priority:
            hot_news_id = int(ret.get('hot_news_id', 0))
            hot_news = NewsHot.objects.filter(id=hot_news_id)
            if hot_news:
                hot_news.update(priority=priority)
                return json_status.result()
            else:
                return json_status.params_error(message='热门新闻不存在')
        return json_status.params_error(message='热门新闻不存在')

    def delete(self, request):
        ret = QueryDict(request.body)
        # print(ret) < QueryDict: {'hot_news_id': ['1']} >
        hot_news_id = int(ret.get('hot_news_id', 0))
        if hot_news_id:
            hot_news = NewsHot.objects.filter(id=hot_news_id)
            if hot_news:
                hot_news.update(is_delete=True)
                return json_status.result()
            else:
                return json_status.params_error(message='热门新闻不存在')
        else:
            return json_status.params_error(message='热门新闻不存在')


# 热门新闻添加
@method_decorator(csrf_exempt, name='dispatch')
class NewsHotAddView(View):
    def get(self, request):
        return render(request, 'news/news_hot_add.html')

    def post(self, request):
        form = NewsHotAddForm(request.POST)
        if form.is_valid():
            news_id = form.cleaned_data.get('news_id')
            priority = form.cleaned_data.get('priority')
            news = News.objects.filter(id=news_id).first()
            if news:
                hot_news = NewsHot.objects.filter(news=news).exists()
                if hot_news:
                    return json_status.params_error(message='热门新闻已存在')
                NewsHot.objects.create(priority=priority, news=news)
                return json_status.result()
            return json_status.params_error(message='新闻不存在')
        else:
            return json_status.params_error(message=form.get_error())


# 新闻编辑
@method_decorator(csrf_exempt, name='dispatch')
class NewsEditView(View):
    def get(self, request):
        news_id = request.GET.get('news_id')
        if news_id:
            news = News.objects.filter(id=news_id).first()
            if news:
                tags = NewsTag.objects.filter(is_delete=False).all()
                return render(request, 'news/newspub.html', context={'news': news, 'tags': tags})
            return json_status.params_error(message='新闻不存在或者已删除')
        return json_status.params_error(message='新闻id不正确')

    def post(self, request):
        form = NewsEditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            tag_id = form.cleaned_data.get('tag_id')
            photo_url = form.cleaned_data.get('photo_url')
            content = form.cleaned_data.get('content')
            news_id = form.cleaned_data.get('news_id')
            news = News.objects.filter(id=news_id, is_delete=False)
            tag = NewsTag.objects.filter(id=tag_id, is_delete=False).first()
            if news and tag:
                news.update(title=title, desc=desc, tag=tag, photo_url=photo_url, content=content, author=request.user)
                return json_status.result()
            else:
                return json_status.params_error(message='新闻不存在')
        else:
            return json_status.params_error(message=form.get_error())
        return render(request, 'news/newspub.html')
