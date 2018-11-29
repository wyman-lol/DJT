from django.core.management.base import BaseCommand
from apps.news.models import NewsHot, News, NewsBanner, NewsComment
from apps.admin_staff.models import NewsTag
from django.contrib.auth.models import Group, Permission, ContentType
from apps.course.models import Course, Teacher, CourseCategory
from apps.doc.models import Doc


#  运营组/课程组/管理员组
#  运营组: 负责发表新闻，日常维护
#  课程组: 负责发布课程，上传文档
#  管理员: 运营组+课程组
class Command(BaseCommand):
    def handle(self, *args, **options):
        # 运营组
        # 会产生一个对象  创建用户的时候 update/delete(返回True/False)
        yy_group = Group.objects.create(name='运营组')
        # 根据模型找权限
        yy_content_types = [
            ContentType.objects.get_for_model(NewsComment),
            ContentType.objects.get_for_model(NewsHot),
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsBanner),
            ContentType.objects.get_for_model(NewsTag),
        ]
        # 查找权限
        yy_permissions = Permission.objects.filter(content_type__in=yy_content_types)
        yy_group.permissions.set(yy_permissions)

        # 课程组
        ck_group = Group.objects.create(name='课程组')
        ck_content_types = [
            ContentType.objects.get_for_model(Doc),
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(Teacher),
        ]
        ck_permissions = Permission.objects.filter(content_type__in=ck_content_types)
        ck_group.permissions.set(ck_permissions)

        # 创建管理员组
        admin_group = Group.objects.create(name='管理员')
        admin_permissions = yy_permissions.union(ck_permissions)
        admin_group.permissions.set(admin_permissions)
        self.stdout.write(self.style.SUCCESS("分组初始化成功"))