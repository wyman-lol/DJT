from django.db import models


# Create your models here.
# 新闻模型表
class News(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    # 保存图片的url地址
    photo_url = models.URLField()
    content = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    # on_delete级连删除
    tag = models.ForeignKey('admin_staff.NewsTag', on_delete=models.CASCADE)
    author = models.ForeignKey('account.User', on_delete=models.CASCADE)

    # 设置按-id排序，filter查询出来的结果就是倒序的
    # 或者在filter后面加order_by（'-id'）
    class Meta:
        ordering = ('-id',)


# 新闻评论模型表
class NewsComment(models.Model):
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    author = models.ForeignKey('account.User', on_delete=models.CASCADE)
    # News反向查询的话就是comment or NewsComment_set
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='comment')

    class Meta:
        ordering = ('-id',)


class NewsHot(models.Model):
    # 和新闻表是一对一关系
    news = models.OneToOneField('News', on_delete=models.CASCADE)
    # 优先级
    priority = models.IntegerField()
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-priority',)
