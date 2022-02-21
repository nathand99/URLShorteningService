from django.contrib import admin
from django.urls import path, re_path

from .views import wildcard_redirect

#url patterns are tried in order
# directs should be last to do some other stuff eg about
urlpatterns = [
    re_path(r'^(?P<path>.*)', wildcard_redirect),
]