from django.conf.urls import patterns, include, url
from django.conf import settings

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MysqlTest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^.*static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH}),
    url(r'^NoticeType/select', 'NoticeType.views.select'),
    url(r'^NoticeType/insert', 'NoticeType.views.insert'),
    url(r'^NoticeType/update', 'NoticeType.views.update'),
    url(r'^NoticeType/modify', 'NoticeType.views.modify'),
    url(r'^NoticeType/delete', 'NoticeType.views.delete'),
    url(r'^MonitorInfo/select', 'MonitorInfo.views.select'),
    url(r'^MonitorInfo/insert', 'MonitorInfo.views.insert'),
    url(r'^MonitorInfo/update', 'MonitorInfo.views.update'),
    url(r'^MonitorInfo/modify', 'MonitorInfo.views.modify'),
    url(r'^MonitorInfo/delete', 'MonitorInfo.views.delete'),
    
)
