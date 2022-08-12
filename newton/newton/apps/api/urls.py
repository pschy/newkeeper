from django.urls import include, re_path

urlpatterns = [
    # system
    re_path(r'^health/', include('system.urls')),
    re_path(r'^key/', include('key.urls')),
]