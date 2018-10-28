"""DJT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from DJT import settings
urlpatterns = [
    path('account/', include('apps.account.urls')),
    path('course/', include('apps.course.urls')),
    path('doc/', include('apps.doc.urls')),
    path('admin/', include('apps.admin_staff.urls')),
    path('news/', include('apps.news.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# static拼接一个路径列表到原来的列表里面，这样就可以访问media里面的文件了

