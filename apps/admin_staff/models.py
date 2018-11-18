from django.db import models

# Create your models here.
class NewsTag(models.Model):

    tag_name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    # 假删
    is_delete = models.BooleanField(default=False)
