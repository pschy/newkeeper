from django.urls import include, re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    re_path(r'^api/v(?P<version>[0-9]+)/', include("api.urls")),
    re_path(r'^filestorage/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]