from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MonitorSystem.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^.*static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH}),
    url(r'^index', 'ShareMethod.views.index'),
    url(r'^SuccessMessage', 'ShareMethod.views.SuccessMessage'),
    url(r'^FailureMessage', 'ShareMethod.views.FailureMessage'),
    url(r'^login$', 'Login.views.login'),
    url(r'^logout$', 'Login.views.logout'),
#     url(r'^SmsSp/select_SmsSp', 'SmsSp.views.select_SmsSp'),
#     url(r'^SmsSp/export_SmsSp', 'SmsSp.views.export_SmsSp'),
    url(r'^SmsCluster/select_cluster', 'SmsCluster.views.select_cluster'),
    url(r'^SmsCluster/export_cluster', 'SmsCluster.views.export_cluster'),
#     url(r'^SmsGate/select_cmpp', 'SmsGate.views.select_cmpp'),
#     url(r'^SmsGate/export_cmpp', 'SmsGate.views.export_cmpp'),
#     url(r'^SmsGate/select_sgip', 'SmsGate.views.select_sgip'),
#     url(r'^SmsGate/export_sgip', 'SmsGate.views.export_sgip'),
#     url(r'^SmsGate/select_smgp', 'SmsGate.views.select_smgp'),
#     url(r'^SmsGate/export_smgp', 'SmsGate.views.export_smgp'),
    url(r'^LogAnalysis/customerSubmit.do', 'LogAnalysis.views.customerSubmit'),
    url(r'^LogAnalysis/customerSpeed.do', 'LogAnalysis.views.customerSpeed'),
    url(r'^LogAnalysis/tdSend.do', 'LogAnalysis.views.tdSend'),
#     url(r'^LogAnalysis/clusterSpeed.do', 'LogAnalysis.views.clusterSpeed'),
#     url(r'^LogAnalysis/clusterSubmit.do', 'LogAnalysis.views.clusterSubmit'),
#     url(r'^LogAnalysis/clusterTdSend.do', 'LogAnalysis.views.clusterTdSend'),
#     url(r'^LogAnalysis/tdOverStock.do', 'LogAnalysis.views.tdOverStock'),
#     url(r'^CommandQuery/CommandQuery.do', 'CommandQuery.views.CommandQuery'),

)
