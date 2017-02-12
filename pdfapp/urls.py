# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import upload_view

urlpatterns = [
    url(r'^upload/$', upload_view, name='upload')
]