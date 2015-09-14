from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'YysBill.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^.*static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH}),
    url(r'^index', 'ShareMethod.views.index'),
    url(r'^SuccessMessage', 'ShareMethod.views.SuccessMessage'),
    url(r'^FailureMessage', 'ShareMethod.views.FailureMessage'),
    url(r'^login$', 'Login.views.login'),
    url(r'^logout$', 'Login.views.logout'),
    url(r'upload.do', 'OpExcel.views.upload'),
    url(r'insert.do', 'OpExcel.views.insert'),
    url(r'select.do', 'OpExcel.views.select'),
    url(r'modify.do', 'OpExcel.views.modify'),
    url(r'update.do', 'OpExcel.views.update'),
)
