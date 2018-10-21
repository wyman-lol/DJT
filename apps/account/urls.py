from django.urls import path
from .views import RegisterView, LoginView, LogoutView, graph_chptcha, sms_send

app_name = 'account'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('loading/', LoginView.as_view(), name='loading'),
    path('out/', LogoutView, name='out_view'),
    path('graph-captcha/', graph_chptcha, name='graph-captcha'),
    path('sms_send/', sms_send, name='sms_send'),
]