# -*- coding: utf-8 -*-

from scan.forms.settings import *
from scan.models import Contest

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render_to_response, RequestContext
from django.http import Http404

@login_required
def index(request, contest_id):
    contest = get_object_or_404(Contest, pk = contest_id)

    context = {'contest_id': contest_id, 'genres': contest.genres.all(), 'users': contest.users.all()}
    return render_to_response('contests/index.html', context, RequestContext(request))

@login_required
def settings_index(request, contest_id):
    return redirect('scan.views.contests.settings', contest_id, 'contest')

@login_required
def settings(request, contest_id, tab):
    tabs = {
        'contest'   :contest_settings,
        'genre'     :genre_settings,
        'user'      :user_settings,
        'user_add'  :user_add_settings,
    }
    if tab in tabs:
        if not request.user.is_staff:
            return redirect('scan.views.index')
        contest = get_object_or_404(Contest, pk = contest_id)
        return tabs[tab](request, contest_id, contest)
    else:
        raise Http404

@login_required
def contest_settings(request, contest_id, contest):
    if request.method == 'POST':
        form = ContestForm(request.POST, instance = contest)
        if form.is_valid():
            contest = form.save()
    form = ContestForm(instance = contest)
    context = {'form': form, 'contest_id': contest_id}
    return render_to_response('settings/contest.html', context, RequestContext(request))

@login_required
def genre_settings(request, contest_id, contest):
    if request.method == 'POST':
        form = ContestGenreForm(request.POST, instance = contest)
        if form.is_valid():
            contest = form.save()
    form = ContestGenreForm(instance = contest)
    context = {'form': form, 'contest_id': contest_id}
    return render_to_response('settings/genre.html', context, RequestContext(request))

@login_required
def user_settings(request, contest_id, contest):
    context = {'contest_id': contest_id, 'users': contest.users.all()}
    return render_to_response('settings/user.html', context, RequestContext(request))

@login_required
def user_add_settings(request, contest_id, contest):
    if request.method == 'POST':
        form = ContestUserForm(contest, request.POST)
        if form.is_valid():
            user = User.objects.get(username = form.data.get('user'))
            contest.users.add(user)
            contest.save()
            return redirect('scan.views.contests.settings', contest_id, 'user')
    else:
        form = ContestUserForm(contest)
    context = {'form': form, 'contest_id': contest_id}
    return render_to_response('settings/user_add.html', context, RequestContext(request))

@login_required
def user_del_settings(request, contest_id, user_id):
    if not request.user.is_staff:
        return redirect('scan.views.index')

    contest = get_object_or_404(Contest, pk = contest_id)
    user = get_object_or_404(User, pk = user_id)
    contest.users.remove(user)

    return redirect('scan.views.contests.settings', contest_id, 'user')

@login_required
def answer(request, contest_id, genre_id):
    pass
