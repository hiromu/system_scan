# -*- coding: utf-8 -*-

from scan.forms.admin import *
from scan.models import Genre

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

@login_required
def index(request):
    return redirect('scan.views.admin.admin', 'general')

@login_required
def admin(request, tab):
    for value in tabs:
        if value[0] == tab:
            if not request.user.is_staff:
                return redirect('scan.views.index')
            return value[1][0](request)
            break
    else:
        raise Http404

@login_required
def general_settings(request):
    context = {'subtitles': [_(u"サイト設定"), _(u"一般設定")], 'page': 'general', 'tabs': tabs}
    return render_to_response('admin/general.html', context, RequestContext(request))

@login_required
def genre_settings(request):
    context = {'subtitles': [_(u"サイト設定"), _(u"ジャンル設定")], 'page': 'genre', 'tabs': tabs, 'genres': Genre.objects.all()}
    return render_to_response('admin/genre.html', context, RequestContext(request))

@login_required
def user_settings(request):
    context = {'subtitles': [_(u"サイト設定"), _(u"ユーザー設定")], 'page': 'user', 'tabs': tabs, 'users': User.objects.all()}
    return render_to_response('admin/user.html', context, RequestContext(request))

@login_required
def genre_add(request):
    if not request.user.is_staff:
        return redirect('scan.views.index')
    if request.method == 'POST':
        form = GenreAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('scan.views.admin.admin', tab = 'genre')
    else:
        form = GenreAddForm()
    context = {'subtitles': [_(u"サイト設定"), _(u"ジャンル追加")], 'form': form, 'page': 'genre', 'tabs': tabs}
    return render_to_response('admin/genre_add.html', context, RequestContext(request))

@login_required
def user_edit(request, user_id):
    if not request.user.is_staff:
        return redirect('scan.views.index')

    user = get_object_or_404(User, pk = user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            return redirect('scan.views.admin.admin', tab = 'user')
    else:
        form = UserEditForm(instance = user)
    context = {'subtitles': [_(u"サイト設定"), _(u"ユーザー設定"), user.username], 'form': form, 'page': 'user', 'tabs': tabs}
    return render_to_response('admin/user_edit.html', context, RequestContext(request))

tabs = (
    ('general'  ,(general_settings, _(u"一般設定"))),
    ('genre'    ,(genre_settings,   _(u"ジャンル設定"))),
    ('user'     ,(user_settings,    _(u"ユーザー設定"))),
)
