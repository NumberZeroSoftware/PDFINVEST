# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import upload_view, edit_view, show_files

urlpatterns = [
    url(r'^upload/$', upload_view, name='upload'),
    #url(r'^edit/(?P<fileName>[^\.\s/]+\.pdf)$', edit_view, name='edit'),
    url(r'^edit/(?P<filePath>[^\.\s]+)/(?P<fileName>[^\.\s/]+)\.pdf$', edit_view, name='edit'),
    url(r'^files/$', show_files, name='files')
]