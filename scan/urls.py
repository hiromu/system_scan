from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'scan.views.index'),

    (r'^contests/(?P<contest_id>\d+)/$', 'scan.views.contests.index'),
    (r'^contests/(?P<contest_id>\d+)/(?P<genre_id>\d+)/$', 'scan.views.contests.problem'),
    (r'^contests/(?P<contest_id>\d+)/(?P<genre_id>\d+)/(?P<problem_id>\d+)/$', 'scan.views.contests.answer'),
    (r'^contests/(?P<contest_id>\d+)/(?P<genre_id>\d+)/finish/$', 'scan.views.contests.finish'),
#   (r'^contests/(?P<contest_id>\d+)/score/$', 'scan.views.score'),

    (r'^contests/add/$', 'scan.views.settings.add'),
    (r'^contests/(?P<contest_id>\d+)/settings/$', 'scan.views.settings.index'),
    (r'^contests/(?P<contest_id>\d+)/settings/user/add/$', 'scan.views.settings.user_add'),
    (r'^contests/(?P<contest_id>\d+)/settings/user/(?P<user_id>\d+)/del/$', 'scan.views.settings.user_del'),
    (r'^contests/(?P<contest_id>\d+)/settings/(?P<tab>\w*)/$', 'scan.views.settings.settings'),

    (r'^contests/(?P<contest_id>\d+)/problems/(?P<genre_id>\d+)/$', 'scan.views.problems.index'),
    (r'^contests/(?P<contest_id>\d+)/problems/(?P<genre_id>\d+)/add/$', 'scan.views.problems.add'),
    (r'^contests/(?P<contest_id>\d+)/problems/(?P<genre_id>\d+)/edit/(?P<problem_id>\d+)/$', 'scan.views.problems.edit'),
    (r'^contests/(?P<contest_id>\d+)/problems/(?P<genre_id>\d+)/del/(?P<problem_id>\d+)/$', 'scan.views.problems.delete'),

#   (r'^contests/(?P<contest_id>\d+)/mark/$', 'scan.views.mark'),

    (r'^accounts/login/$', 'scan.views.accounts.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^accounts/profile/$', 'scan.views.accounts.profile'),

    (r'^admin/$', 'scan.views.admin.index'),
    (r'^admin/database/', include(admin.site.urls)),
    (r'^admin/genre/add/$', 'scan.views.admin.genre_add'),
    (r'^admin/user/edit/(?P<user_id>\d+)/$', 'scan.views.admin.user_edit'),
    (r'^admin/(?P<tab>\w*)/$', 'scan.views.admin.admin'),
)
