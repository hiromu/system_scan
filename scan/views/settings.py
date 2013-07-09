# -*- coding: utf-8 -*-

from system_scan.scan.forms import *
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
		form = ContestForm(request.POST)
		if form.is_valid():
			contest = form.save(commit = False)
			contest.pk = contest_id
			contest.save()
	
	form = ContestForm(instance = contest)
	context = {'form': form, 'contest_id': contest_id}
	return render_to_response('settings/contest.html', context, RequestContext(request))

@login_required
def genre(request, contest_id):
	if not request.user.is_staff:
		return redirect('system_scan.scan.views.index')

	contest = get_object_or_404(Contest, pk = contest_id)
	if request.method == 'POST':
		form = ContestGenreForm(request.POST)
		if form.is_valid():
			contest = form.save(commit = False)
			contest.pk = contest_id
			contest.save()
	
	form = ContestGenreForm(instance = contest)
	context = {'form': form, 'contest_id': contest_id}
	return render_to_response('settings/genre.html', context, RequestContext(request))

@login_required
def user(request, contest_id):
	if not request.user.is_staff:
		return redirect('system_scan.scan.views.index')

	contest = get_object_or_404(Contest, pk = contest_id)
	privileges = Privilege.objects.filter(contest = contest)
	
	context = {'contest_id': contest_id, 'privileges': privileges}
	return render_to_response('settings/user.html', context, RequestContext(request))

@login_required
def user_add(request, contest_id):
	if not request.user.is_staff:
		return redirect('system_scan.scan.views.index')

	contest = get_object_or_404(Contest, pk = contest_id)
	if request.method == 'POST':
		form = PrivilegeForm(contest, request.POST)
		if form.is_valid():
			privilege = form.save(commit = False)
			privilege.contest = contest
			privilege.save()
			return redirect('system_scan.scan.views.settings.user', contest_id)
	else:
		form = PrivilegeForm(contest)

	context = {'form': form, 'contest_id': contest_id}
	return render_to_response('settings/user_add.html', context, RequestContext(request))

@login_required
def user_del(request, contest_id, user_id):
	if not request.user.is_staff:
		return redirect('system_scan.scan.views.index')

	contest = get_object_or_404(Contest, pk = contest_id)
	user = get_object_or_404(User, pk = user_id)
	Privilege.objects.filter(contest = contest, user = user).delete()

	return redirect('system_scan.scan.views.settings.user', contest_id)
