from django.conf.urls import patterns, include, url
from settings import DEBUG
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('ask.views',
    # Examples:
    # url(r'^$', 'ask_qst.views.home', name='home'),
    # url(r'^ask_qst/', include('ask_qst.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
     url(r'^$', 'index'),
    url(r'^([0-9]+)/$', 'index'),
    url(r'^qst/([0-9]+)/$', 'questions'),
    url(r'^reg/$', 'regestration'),
    url(r'^enter/$', 'enter'),
    url(r'^test/$', 'test'),
    url(r'^sid/$', 'get_user'),
    url(r'^logout/$', 'logout'),
	url(r'^like/$', 'like'),
	url(r'^answers/$', 'answers'),
	url(r'^user/([0-9]+)/$', 'user_info'),
	url(r'^topics/$', 'topics'),
	url(r'^topic/([0-9]+)/$', 'topic'),
	url(r'^right/$', 'rightAnswer'),
	url(r'^testreg/$', 'test_reg'),
	url(r'^ask/$', 'ask'),
	url(r'^addask/$', 'addask'),
	url(r'^qstadd/$', 'qstadd'),
	url(r'^client/$', 'client'),
)


    
