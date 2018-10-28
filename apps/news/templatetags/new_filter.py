from django import template
from django.utils.timezone import now
from datetime import datetime

register = template.Library()


@register.filter
def date_format(val):
    if isinstance(val, datetime):
        time = now() - val
        # 间隔总秒数
        sec = time.total_seconds()
    else:
        return val
    if sec < 60:
        return '刚刚'
    elif 60 <= sec < 60 * 60:
        return '{:.0f}分钟前'.format(sec / 60)
    elif 60 * 60 <= sec < 60 * 60 * 24:
        return '{:.0f}小时前'.format(sec / 3600)
    else:
        return val.strftime('%Y-%m-%d %H:%M')
