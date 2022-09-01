from django.urls import include, re_path
from system import apis

urlpatterns = [
    re_path(r'^$', apis.api_ping),
    re_path(r'^ip/$', apis.api_get_ip),
    re_path(r'^version/$', apis.api_show_version),
]
