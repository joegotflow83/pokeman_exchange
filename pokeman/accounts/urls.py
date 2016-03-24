from django.conf.urls import url
from django.contrib.auth import views as auth_views

from accounts import views


urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^signup/$', views.Signup.as_view(), name='signup'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
]
