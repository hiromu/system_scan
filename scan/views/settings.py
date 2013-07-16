# -*- coding: utf-8 -*-

from scan.forms.settings import ContestForm, ContestGenreForm, ContestUserForm
from scan.models import Contest

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

@login_required
def add(request):
    if not request.user.is_staff:
        return redirect('scan.views.index')

    if request.method == 'POST':
        form = ContestForm(request.POST)
        if form.is_valid():
            contest = form.save()
            return redirect('scan.views.settings.index', contest_id = contest.id)
    else:
        form = ContestForm()

    context = {'form': form}
    return render_to_response('settings/add.html', context, RequestContext(request))

@login_required
def index(request, contest_id):
    return redirect('scan.views.settings.settings', contest_id, 'contest')

@login_required
def settings(request, contest_id, tab):
    for value in tabs:
        if value[0] == tab:
            if not request.user.is_staff:
                return redirect('scan.views.index')
            contest = get_object_or_404(Contest, pk = contest_id)
            return value[1][0](request, contest_id, contest)
            break
    else:
        raise Http404

def contest_settings(request, contest_id, contest):
    if request.method == 'POST':
        form = ContestForm(request.POST, instance = contest)
        if form.is_valid():
            contest = form.save()
    else:
        form = ContestForm(instance = contest)
    context = {'subtitles': [contest.name, _(u'一般設定')], 'contest': contest, 'form': form, 'page': 'contest', 'tabs': tabs}
    return render_to_response('settings/contest.html', context, RequestContext(request))

def genre_settings(request, contest_id, contest):
    if request.method == 'POST':
        form = ContestGenreForm(request.POST, instance = contest)
        if form.is_valid():
            contest = form.save()
    else:
        form = ContestGenreForm(instance = contest)
    context = {'subtitles': [contest.name, _(u'問題設定')], 'contest': contest, 'form': form, 'page': 'genre', 'tabs': tabs}
    return render_to_response('settings/genre.html', context, RequestContext(request))

def user_settings(request, contest_id, contest):
    context = {'subtitles': [contest.name, _(u'ユーザー設定')], 'contest': contest, 'page': 'user', 'users': contest.users.all(), 'tabs': tabs}
    return render_to_response('settings/user.html', context, RequestContext(request))

@login_required
def user_add(request, contest_id):
    if not request.user.is_staff:
        return redirect('scan.views.index')

    contest = get_object_or_404(Contest, pk = contest_id)
    if request.method == 'POST':
        form = ContestUserForm(contest, request.POST)
        if form.is_valid():
            user = User.objects.get(username = form.data.get('user'))
            contest.users.add(user)
            contest.save()
            return redirect('scan.views.settings.settings', contest_id, 'user')
    else:
        form = ContestUserForm(contest)
    context = {'subtitles': [contest.name, _(u'ユーザー追加')], 'contest': contest, 'form': form, 'page': 'user', 'tabs': tabs}
    return render_to_response('settings/user_add.html', context, RequestContext(request))

@login_required
def user_del(request, contest_id, user_id):
    if not request.user.is_staff:
        return redirect('scan.views.index')

    contest = get_object_or_404(Contest, pk = contest_id)
    user = get_object_or_404(User, pk = user_id)
    contest.users.remove(user)

    return redirect('scan.views.settings.settings', contest_id, 'user')

tabs = (
    ('contest'   ,(contest_settings,    _(u'一般設定'))),
    ('genre'     ,(genre_settings,      _(u'問題設定'))),
    ('user'      ,(user_settings,       _(u'ユーザー設定'))),
)
