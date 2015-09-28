from django.conf.urls import patterns, include, url
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HelloDjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^blog/index/$', 'blog.views.index'),
     url(r'^blog/show_author/$','blog.views.show_author'),
     url(r'^blog/show_book/$','blog.views.show_book'),
     url(r'^blog/register/$','blog.views.register'),
)
