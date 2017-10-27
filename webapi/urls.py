#! usr/bin/env python
# encoding: utf-8

from django.conf.urls import url
from webapi.views import *

urlpatterns = [
    url(r'^html$', finger_point_test_html_01),
    url(r'^finger_01$', finger_point_test_api_01),
    url(r'^finger_02$', finger_point_test_api_02),
    url(r'^list', finger_point_test_file_list),
]