# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import upload_view, edit_view, show_files, sigpae, sigpae_show, sigpae_report, ref_report

urlpatterns = [
    url(r'^upload/$', upload_view, name='upload'),
    #url(r'^edit/(?P<fileName>[^\.\s/]+\.pdf)$', edit_view, name='edit'),
    url(r'^edit/(?P<filePath>[^\.\s]+)/(?P<fileName>[^\.\s/]+)\.pdf$', edit_view, name='edit'),
    url(r'^files/$', show_files, name='files'),
    url(r'^sigpae/$', sigpae, name='sigpae'),
    url(r'^sigpae/(?P<pk>[0-9]+)$', sigpae_show, name='sigpae_show'),
    url(r'^report/global/$', sigpae_report, name='global_report'),
    url(r'^report/ref/$', ref_report, name='ref_report'),
]
