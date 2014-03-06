from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'scan.views.index'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
    url(r'^favicon\.svg$', RedirectView.as_view(url='/static/img/favicon.svg')),

    url(r'^contests/(?P<contest_id>\d+)/$', 'scan.views.contests.index'),
    url(r'^contests/(?P<contest_id>\d+)/(?P<genre_id>\d+)/$', 'scan.views.contests.problem'),
    url(r'^contests/(?P<contest_id>\d+)/(?P<genre_id>\d+)/(?P<problem_id>\d+)/$', 'scan.views.contests.answer'),
    url(r'^contests/(?P<contest_id>\d+)/(?P<genre_id>\d+)/finish/$', 'scan.views.contests.finish'),
    url(r'^contests/(?P<contest_id>\d+)/ranking/$', 'scan.views.contests.ranking'),
    url(r'^contests/(?P<contest_id>\d+)/ranking/detail/$', 'scan.views.contests.detail'),

    url(r'^contests/add/$', 'scan.views.settings.add'),
    url(r'^contests/(?P<contest_id>\d+)/settings/$', 'scan.views.settings.index'),
    url(r'^contests/(?P<contest_id>\d+)/settings/user/add/$', 'scan.views.settings.user_add'),
    url(r'^contests/(?P<contest_id>\d+)/settings/user/(?P<user_id>\d+)/del/$', 'scan.views.settings.user_del'),
    url(r'^contests/(?P<contest_id>\d+)/settings/(?P<tab>\w*)/$', 'scan.views.settings.settings'),

    url(r'^contests/(?P<contest_id>\d+)/problems/(?P<genre_id>\d+)/$', 'scan.views.problems.index'),
    url(r'^contests/(?P<contest_id>\d+)/problems/(?P<genre_id>\d+)/rearrange/$', 'scan.views.problems.rearrange'),
    url(r'^contests/(?P<contest_id>\d+)/problems/(?P<genre_id>\d+)/add/$', 'scan.views.problems.add'),
    url(r'^contests/(?P<contest_id>\d+)/problems/(?P<genre_id>\d+)/edit/(?P<problem_id>\d+)/$', 'scan.views.problems.edit'),
    url(r'^contests/(?P<contest_id>\d+)/problems/(?P<genre_id>\d+)/edit/(?P<problem_id>\d+)/preview/$', 'scan.views.problems.preview'),
    url(r'^contests/(?P<contest_id>\d+)/problems/(?P<genre_id>\d+)/edit/(?P<problem_id>\d+)/post_comment/$', 'scan.views.problems.post_comment'),
    url(r'^contests/(?P<contest_id>\d+)/problems/(?P<genre_id>\d+)/del/(?P<problem_id>\d+)/$', 'scan.views.problems.delete'),
    url(r'^contests/(?P<contest_id>\d+)/problems/(?P<genre_id>\d+)/figures/(?P<problem_id>\d+)/get/$', 'scan.views.problems.get_figures'),
    url(r'^contests/(?P<contest_id>\d+)/problems/(?P<genre_id>\d+)/figures/(?P<problem_id>\d+)/add/$', 'scan.views.problems.add_figure'),
    url(r'^contests/(?P<contest_id>\d+)/problems/(?P<genre_id>\d+)/figures/(?P<problem_id>\d+)/del/(?P<figure_id>\d+)/$', 'scan.views.problems.delete_figure'),

    url(r'^contests/(?P<contest_id>\d+)/marks/(?P<genre_id>\d+)/$', 'scan.views.marks.index'),
    url(r'^contests/(?P<contest_id>\d+)/marks/(?P<genre_id>\d+)/(?P<problem_id>\d+)/$', 'scan.views.marks.problem'),
    url(r'^contests/(?P<contest_id>\d+)/marks/(?P<genre_id>\d+)/(?P<problem_id>\d+)/(?P<answer_id>\d+)/$', 'scan.views.marks.mark'),
    url(r'^contests/(?P<contest_id>\d+)/marks/(?P<genre_id>\d+)/(?P<problem_id>\d+)/finish/$', 'scan.views.marks.finish'),

    url(r'^accounts/login/$', 'scan.views.accounts.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/profile/$', 'scan.views.accounts.profile'),

    url(r'^admin/$', 'scan.views.admin.index'),
    url(r'^admin/database/', include(admin.site.urls)),
    url(r'^admin/genre/add/$', 'scan.views.admin.genre_add'),
    url(r'^admin/user/edit/(?P<user_id>\d+)/$', 'scan.views.admin.user_edit'),
    url(r'^admin/(?P<tab>\w*)/$', 'scan.views.admin.admin'),
)
