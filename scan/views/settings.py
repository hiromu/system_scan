# -*- coding: utf-8 -*-

from system_scan.scan.forms.settings import *
from system_scan.scan.models import *

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

@login_required
def index(request):
    if not request.user.is_staff:
        return redirect('system_scan.scan.views.index')

    if request.method == 'POST':
        form = ContestForm(request.POST)
        if form.is_valid():
            contest = form.save()
            return redirect('system_scan.scan.views.settings.contest', contest_id = contest.id)
    else:
        form = ContestForm()

    context = {'form': form}
    return render_to_response('settings/index.html', context, RequestContext(request))

@login_required
def contest(request, contest_id):
    if not request.user.is_staff:
        return redirect('system_scan.scan.views.index')

    contest = get_object_or_404(Contest, pk = contest_id)
    if request.method == 'POST':
        form = ContestForm(request.POST, instance = contest)
        if form.is_valid():
            contest = form.save()
    
    form = ContestForm(instance = contest)
    context = {'form': form, 'contest_id': contest_id}
    return render_to_response('settings/contest.html', context, RequestContext(request))

@login_required
def genre(request, contest_id):
    if not request.user.is_staff:
        return redirect('system_scan.scan.views.index')

    contest = get_object_or_404(Contest, pk = contest_id)
    if request.method == 'POST':
        form = ContestGenreForm(request.POST, instance = contest)
        if form.is_valid():
            contest = form.save()
    
    form = ContestGenreForm(instance = contest)
    context = {'form': form, 'contest_id': contest_id}
    return render_to_response('settings/genre.html', context, RequestContext(request))

@login_required
def user(request, contest_id):
    if not request.user.is_staff:
        return redirect('system_scan.scan.views.index')

    contest = get_object_or_404(Contest, pk = contest_id)
    
    context = {'contest_id': contest_id, 'users': contest.users.all()}
    return render_to_response('settings/user.html', context, RequestContext(request))

@login_required
def user_add(request, contest_id):
    if not request.user.is_staff:
        return redirect('system_scan.scan.views.index')

    contest = get_object_or_404(Contest, pk = contest_id)
    if request.method == 'POST':
        form = ContestUserForm(contest, request.POST)
        if form.is_valid():
            user = User.objects.get(username = form.data.get('user'))
            contest.users.add(user)
            contest.save()
            return redirect('system_scan.scan.views.settings.user', contest_id)
    else:
        form = ContestUserForm(contest)

    context = {'form': form, 'contest_id': contest_id}
    return render_to_response('settings/user_add.html', context, RequestContext(request))

@login_required
def user_del(request, contest_id, user_id):
    if not request.user.is_staff:
        return redirect('system_scan.scan.views.index')

    contest = get_object_or_404(Contest, pk = contest_id)
    user = get_object_or_404(User, pk = user_id)
    contest.users.remove(user)

    return redirect('system_scan.scan.views.settings.user', contest_id)
