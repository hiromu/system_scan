from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'scan.views.index'),

    (r'^(?P<contest_id>\d+)/$', 'scan.views.contests.index'),
#   (r'^(?P<contest_id>\d+)/(?P<genre_id>\d+)/$', 'scan.views.answer'),
#   (r'^(?P<contest_id>\d+)/score/$', 'scan.views.score'),

    (r'^accounts/login/$', 'scan.views.accounts.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^accounts/profile/$', 'scan.views.accounts.profile'),

#   (r'^mark/(?P<contest_id>\d+)/$', 'scan.views.mark_top'),
#   (r'^mark/(?P<contest_id>\d+)/(?P<user_id>\d+)/$', 'scan.views.mark_user'),
#   (r'^mark/(?P<contest_id>\d+)/(?P<user_id>\d+)/(?P<genre_id>\d+)/$', 'scan.views.mark'),

    (r'^settings/$', 'scan.views.settings.index'),
    (r'^settings/(?P<contest_id>\d+)/$', 'scan.views.settings.contest'),
    (r'^settings/(?P<contest_id>\d+)/(?P<genre_id>\d+)/$', 'scan.views.settings.problem'),
    (r'^settings/(?P<contest_id>\d+)/genre/$', 'scan.views.settings.genre'),
    (r'^settings/(?P<contest_id>\d+)/user/$', 'scan.views.settings.user'),
    (r'^settings/(?P<contest_id>\d+)/user/add/$', 'scan.views.settings.user_add'),
    (r'^settings/(?P<contest_id>\d+)/user/del/(?P<user_id>\d+)/$', 'scan.views.settings.user_del'),

#   (r'^admin/$', 'scan.views.admin'),
    (r'^admin/database/', include(admin.site.urls)),
)
