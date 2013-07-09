# -*- coding: utf-8 -*-

from system_scan.scan.forms import *

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
	
	contest_form = ContestForm(instance = contest)
	context = {'contest_form': contest_form}
	return render_to_response('settings/contest.html', context, RequestContext(request))
