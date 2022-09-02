from django.urls import include, re_path
from django.views.static import serve
from django.conf import settings
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newkeeper.settings")
django.setup()

urlpatterns = [
    re_path(r'^api/v(?P<version>[0-9]+)/', include("api.urls")),
    re_path(r'^filestorage/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]
