from django.db import models

# Create your models here.

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