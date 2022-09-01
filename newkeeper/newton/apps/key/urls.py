from django.urls import include, re_path
from key import apis

urlpatterns = [
    re_path(r'^$', apis.api_get),
    re_path(r'^generator$', apis.api_generator),
    re_path(r'^bind$', apis.api_bind),
]

