from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'system_scan.views.home', name='home'),
    # url(r'^system_scan/', include('system_scan.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

	(r'^$', 'system_scan.scan.views.index'),
	(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
	(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

	(r'^(?P<contest_id>\d+)/$', 'system_scan.scan.views.contest'),
	(r'^(?P<contest_id>\d+)/(?P<genre_id>\d+)/$', 'system_scan.scan.views.answer'),
	(r'^(?P<contest_id>\d+)/score/$', 'system_scan.scan.views.scre'),

	(r'^mark/(?P<contest_id>\d+)/$', 'system_scan.scan.views.mark_top'),
	(r'^mark/(?P<contest_id>\d+)/(?P<user_id>\d+)/$', 'system_scan.scan.views.mark_user'),
	(r'^mark/(?P<contest_id>\d+)/(?P<user_id>\d+)/(?P<genre_id>\d+)/$', 'system_scan.scan.views.mark'),
	
	(r'^setting/$', 'system_scan.scan.views.setting'),
	(r'^setting/(?P<contest_id>\d+)/$', 'system_scan.scan.views.setting_contest'),
	(r'^setting/(?P<contest_id>\d+)/(?P<genre_id>\d+)/$', 'system_scan.scan.views.setting_problem'),

	(r'^admin/$', 'system_scan.scan.views.admin'),
	(r'^admin/database/', include(admin.site.urls)),
)
