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

#   (r'^(?P<contest_id>\d+)/$', 'system_scan.scan.views.contest'),
#   (r'^(?P<contest_id>\d+)/(?P<genre_id>\d+)/$', 'system_scan.scan.views.answer'),
#   (r'^(?P<contest_id>\d+)/score/$', 'system_scan.scan.views.score'),

    (r'^accounts/login/$', 'system_scan.scan.views.accounts.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^accounts/profile/$', 'system_scan.scan.views.accounts.profile'),

#   (r'^mark/(?P<contest_id>\d+)/$', 'system_scan.scan.views.mark_top'),
#   (r'^mark/(?P<contest_id>\d+)/(?P<user_id>\d+)/$', 'system_scan.scan.views.mark_user'),
#   (r'^mark/(?P<contest_id>\d+)/(?P<user_id>\d+)/(?P<genre_id>\d+)/$', 'system_scan.scan.views.mark'),
    
    (r'^settings/$', 'system_scan.scan.views.settings.index'),
    (r'^settings/(?P<contest_id>\d+)/$', 'system_scan.scan.views.settings.contest'),
#   (r'^settings/(?P<contest_id>\d+)/(?P<genre_id>\d+)/$', 'system_scan.scan.views.setting_problem'),
    (r'^settings/(?P<contest_id>\d+)/genre/$', 'system_scan.scan.views.settings.genre'),
    (r'^settings/(?P<contest_id>\d+)/user/$', 'system_scan.scan.views.settings.user'),
    (r'^settings/(?P<contest_id>\d+)/user/add/$', 'system_scan.scan.views.settings.user_add'),
    (r'^settings/(?P<contest_id>\d+)/user/del/(?P<user_id>\d+)/$', 'system_scan.scan.views.settings.user_del'),
    
#   (r'^admin/$', 'system_scan.scan.views.admin'),
    (r'^admin/database/', include(admin.site.urls)),
)
